// SpinZoeker - laat de robotspin een voorwerp zoeken met de camera.
// Elke ronde: foto van de spin -> Claude (CLI) kijkt en kiest een actie -> Piper leest
// in het Nederlands voor wat de spin ziet en doet -> de spin voert de actie uit.
//
//   dotnet run -- [voorwerp] [--host spin.local] [--model sonnet] [--stappen 30]
using System.Diagnostics;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Text.Json;

namespace SpinZoeker;

record Options(string Host, string Model, int MaxSteps, string? Target);

record Decision(string Zie, bool Gevonden, string Positie, string Afstand, string Actie, double Seconden, string Zeg);

static class Program
{
    static Spider spider = null!;
    static Speaker speaker = null!;

    static async Task<int> Main(string[] args)
    {
        Console.OutputEncoding = Encoding.UTF8;
        var opt = ParseArgs(args);
        var tools = FindTools();
        spider = new Spider(opt.Host);
        speaker = new Speaker(tools);

        Console.CancelKeyPress += (_, e) =>
        {
            // always stop the legs, whatever happens
            try { spider.Send("move 10"); } catch { }
            Info("Gestopt (Ctrl+C).", ConsoleColor.Yellow);
        };

        Info($"SpinZoeker - spin: {opt.Host}, model: {opt.Model}", ConsoleColor.Cyan);
        try { Info("Spin zegt: " + spider.Send("ping")); }
        catch (Exception e) { Info($"Kan de spin niet bereiken op {opt.Host}:1337 ({e.Message})", ConsoleColor.Red); return 1; }

        var target = opt.Target;
        while (true)
        {
            if (string.IsNullOrWhiteSpace(target))
            {
                Console.Write("\nWat moet de spin zoeken? (leeg = stoppen) > ");
                target = Console.ReadLine()?.Trim('\uFEFF', ' ', '\t');
                if (string.IsNullOrWhiteSpace(target)) break;
            }
            try { await Search(target!, opt); }
            catch (Exception e)
            {
                Info("Fout tijdens zoeken: " + e.Message, ConsoleColor.Red);
                spider.TryStop();
            }
            target = null;
        }
        try { spider.Send("move 10"); spider.Send("smde 1"); } catch { }
        await speaker.SayAsync("Doei! Tot de volgende keer.");
        return 0;
    }

    static async Task Search(string target, Options opt)
    {
        var session = Path.Combine(Path.GetTempPath(), "spinzoeker", DateTime.Now.ToString("yyyyMMdd-HHmmss"));
        Directory.CreateDirectory(session);
        Info($"\n=== Zoeken naar: {target}   (foto's: {session})", ConsoleColor.Cyan);

        spider.Send("smde 1");          // normal walking mode, legs in
        spider.Send("smul 3");
        await speaker.SayAsync($"Ik ga op zoek naar {target}!");

        var history = new List<string>();
        Task speech = Task.CompletedTask;
        int turnsWithoutSeeing = 0;

        for (int step = 1; step <= opt.MaxSteps; step++)
        {
            var photo = Path.Combine(session, $"stap{step:00}.jpg");
            try { await spider.SnapshotAsync(photo); }
            catch (Exception e) { Info("Geen camerabeeld: " + e.Message, ConsoleColor.Red); await speaker.SayAsync("Oei, mijn camera doet het niet."); return; }

            Info($"\n[stap {step}] Claude kijkt...", ConsoleColor.DarkGray);
            var d = await Ask(opt.Model, target, photo, history, step, opt.MaxSteps);
            Info($"  ziet: {d.Zie}");
            Info($"  gevonden={d.Gevonden} positie={d.Positie} afstand={d.Afstand} -> {d.Actie} {d.Seconden:0.#}s", ConsoleColor.Green);
            history.Add($"stap {step}: zag '{d.Zie}', gevonden={d.Gevonden}, positie={d.Positie}, afstand={d.Afstand}, deed {d.Actie} {d.Seconden:0.#}s");

            await speech;                               // don't talk over the previous sentence
            Info($"  zegt: \"{d.Zeg}\"", ConsoleColor.Magenta);
            speech = speaker.SayAsync(d.Zeg);

            if (d.Actie == "klaar")
            {
                await speech;
                await Found(target);
                return;
            }

            turnsWithoutSeeing = d.Gevonden ? 0 : turnsWithoutSeeing + (d.Actie.StartsWith("draai") ? 1 : 0);
            if (turnsWithoutSeeing >= 14)
            {
                await speech;
                await speaker.SayAsync($"Ik heb overal rondgekeken, maar ik kan {target} niet vinden. Misschien ligt het ergens anders?");
                return;
            }

            try { await spider.DoAsync(d.Actie, d.Seconden); }
            catch (Exception e)
            {
                Info("  Spin reageert niet: " + e.Message, ConsoleColor.Red);
                spider.TryStop();
                await speech;
                await speaker.SayAsync("Oei, mijn pootjes luisteren even niet. Ik stop met zoeken.");
                return;
            }
        }
        await speech;
        await speaker.SayAsync($"Ik ben moe van het zoeken. Ik heb {target} nog niet gevonden.");
        spider.Send("move 10");
    }

    static async Task Found(string target)
    {
        Info("  *** GEVONDEN - poot uitsteken ***", ConsoleColor.Yellow);
        spider.Send("move 10");
        var say = speaker.SayAsync($"Gevonden! Kijk, ik steek mijn poot uit naar {target}!");
        spider.Send("smde 5");          // balloon-race start pose: front legs reach forward
        await say;
        spider.Send("horn");
        await Task.Delay(6000);
        await speaker.SayAsync("Hoera! Zullen we nog iets zoeken?");
        spider.Send("smde 1");          // legs back, ready for the next search
    }

    // ------------------------------------------------------------------ Claude
    static async Task<Decision> Ask(string model, string target, string photo, List<string> history, int step, int maxSteps)
    {
        var recent = history.Count == 0 ? "(nog niets)" : string.Join("\n", history.TakeLast(6));
        var prompt = $$"""
            Je bent het brein van een zespotige robotspin die met een camera op vloerhoogte door een kamer loopt.
            Een kind luistert mee. Opdracht: zoek "{{target}}".

            Bekijk de camerafoto: {{photo}}
            (De camera kijkt recht vooruit. Links in de foto = links van de spin.)

            Wat de spin kan:
            - draai_links / draai_rechts: draait op de plek, ongeveer 12 graden per seconde. 2,5 s is ongeveer 30 graden.
              Blijf tijdens het rondkijken steeds dezelfde kant op draaien (draai_links, 2.5 s): wisselen van
              draairichting laat de spin eerst een stukje terugdraaien.
            - vooruit: loopt naar voren (trekt daarbij een beetje naar links af). 1-4 s.
            - achteruit: 1-3 s.
            - klaar: het voorwerp staat recht voor de spin, ongeveer in het midden en heel dichtbij
              (het vult een groot deel van de foto of de onderkant raakt bijna de onderrand). Dan steekt de spin zijn poot uit.

            Regels:
            - Voorwerp niet in beeld: draai_links 2.5 s.
            - Voorwerp links in beeld: draai_links 1.5 s. Rechts in beeld: draai_rechts 1.5 s.
            - Voorwerp in het midden maar nog ver/middelver: vooruit (ver 3 s, middelver 2 s, dichtbij 1 s).
            - Staat het voorwerp dichtbij en maar een klein beetje links of rechts van het midden: geldt als midden, loop gewoon vooruit.
              Draai alleen bij als het duidelijk aan de zijkant staat (in het buitenste kwart van de foto). Vermijd heen-en-weer draaien:
              als je in de vorige stap de andere kant op draaide, loop dan liever vooruit.
            - Twijfel je of iets het voorwerp is? Kies het meest waarschijnlijke en ga er dichterbij kijken.
            - Pas op voor botsen: staat er vlak voor de spin iets anders in de weg, draai eromheen.

            Wat er tot nu toe gebeurde (stap {{step}} van max {{maxSteps}}):
            {{recent}}

            Antwoord met ALLEEN dit JSON-object, zonder uitleg of codeblok:
            {"zie":"wat je ziet, max 20 woorden","gevonden":true of false,"positie":"links|midden|rechts|geen",
             "afstand":"ver|middel|dichtbij|heel dichtbij|onbekend","actie":"draai_links|draai_rechts|vooruit|achteruit|klaar",
             "seconden":getal,"zeg":"een korte, vrolijke zin voor een kind van ongeveer 5 jaar, in de ik-vorm als de spin, max 20 woorden, over wat je ziet en gaat doen"}
            """;

        for (int attempt = 1; attempt <= 2; attempt++)
        {
            try
            {
                var text = await RunClaude(model, prompt, Path.GetDirectoryName(photo)!);
                var json = ExtractJson(text);
                using var doc = JsonDocument.Parse(json);
                var r = doc.RootElement;
                string S(string n, string def) => r.TryGetProperty(n, out var v) && v.ValueKind == JsonValueKind.String ? v.GetString()! : def;
                var actie = S("actie", "draai_links").Trim().ToLowerInvariant();
                if (actie is not ("draai_links" or "draai_rechts" or "vooruit" or "achteruit" or "klaar")) actie = "draai_links";
                double sec = r.TryGetProperty("seconden", out var sv) && sv.TryGetDouble(out var x) ? x : 2.5;
                bool found = r.TryGetProperty("gevonden", out var gv) && gv.ValueKind == JsonValueKind.True;
                return new Decision(S("zie", "?"), found, S("positie", "geen"), S("afstand", "onbekend"), actie, sec, S("zeg", "Ik kijk nog even verder."));
            }
            catch (Exception e)
            {
                Info($"  (Claude-antwoord niet bruikbaar, poging {attempt}: {e.Message})", ConsoleColor.DarkYellow);
            }
        }
        return new Decision("?", false, "geen", "onbekend", "draai_links", 2.5, "Hmm, ik zie het niet goed. Ik draai een stukje.");
    }

    static async Task<string> RunClaude(string model, string prompt, string workDir)
    {
        var psi = new ProcessStartInfo("claude")
        {
            WorkingDirectory = workDir,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            RedirectStandardInput = true,
            UseShellExecute = false,
            StandardOutputEncoding = Encoding.UTF8,
        };
        foreach (var a in new[] { "-p", "--model", model, "--allowedTools", "Read", "--output-format", "json" }) psi.ArgumentList.Add(a);
        using var p = Process.Start(psi)!;
        await p.StandardInput.WriteAsync(prompt);   // prompt via stdin: no quoting issues
        p.StandardInput.Close();
        var outTask = p.StandardOutput.ReadToEndAsync();
        var errTask = p.StandardError.ReadToEndAsync();
        if (!p.WaitForExit(120_000)) { p.Kill(true); throw new TimeoutException("claude gaf geen antwoord binnen 2 minuten"); }
        var stdout = await outTask;
        if (p.ExitCode != 0) throw new Exception($"claude exit {p.ExitCode}: {(await errTask).Trim()} {stdout.Trim()}");
        using var doc = JsonDocument.Parse(stdout);
        return doc.RootElement.GetProperty("result").GetString() ?? "";
    }

    static string ExtractJson(string s)
    {
        int a = s.IndexOf('{'), b = s.LastIndexOf('}');
        if (a < 0 || b <= a) throw new FormatException("geen JSON in antwoord: " + s);
        return s[a..(b + 1)];
    }

    // ------------------------------------------------------------------ misc
    static Options ParseArgs(string[] args)
    {
        string host = "spin.local", model = "sonnet"; int steps = 40; var words = new List<string>();
        for (int i = 0; i < args.Length; i++)
        {
            switch (args[i])
            {
                case "--host": host = args[++i]; break;
                case "--model": model = args[++i]; break;
                case "--stappen": steps = int.Parse(args[++i]); break;
                default: words.Add(args[i]); break;
            }
        }
        var t = string.Join(' ', words).Trim('\uFEFF', ' ');
        return new Options(host, model, steps, t.Length > 0 ? t : null);
    }

    static string FindTools()
    {
        for (var dir = new DirectoryInfo(AppContext.BaseDirectory); dir != null; dir = dir.Parent)
        {
            var t = Path.Combine(dir.FullName, "tools");
            if (File.Exists(Path.Combine(t, "piper", "piper.exe"))) return t;
        }
        throw new DirectoryNotFoundException("map 'tools' met piper\\piper.exe niet gevonden");
    }

    public static void Info(string s, ConsoleColor c = ConsoleColor.Gray)
    {
        var old = Console.ForegroundColor; Console.ForegroundColor = c; Console.WriteLine(s); Console.ForegroundColor = old;
    }
}

/// <summary>TCP protocol of spInOS (port 1337) + camera snapshot over HTTP (port 8080).</summary>
class Spider(string host)
{
    static readonly HttpClient Http = new() { Timeout = TimeSpan.FromSeconds(40) };

    /// <summary>Send with retries; a busy Pi 1 sometimes answers late.</summary>
    public string Send(string cmd)
    {
        Exception? last = null;
        for (int attempt = 1; attempt <= 3; attempt++)
        {
            try { return SendOnce(cmd); }
            catch (Exception e) { last = e; Thread.Sleep(1000); }
        }
        throw new IOException($"spin antwoordt niet op '{cmd}'", last);
    }

    /// <summary>Stop the legs; never throws.</summary>
    public bool TryStop()
    {
        try { Send("move 10"); return true; } catch { return false; }
    }

    string SendOnce(string cmd)
    {
        using var c = new TcpClient();
        c.Connect(host, 1337);
        var s = c.GetStream();
        s.ReadTimeout = 20000;
        var b = Encoding.UTF8.GetBytes(cmd + "<EOF>");
        s.Write(b);
        var sb = new StringBuilder(); var buf = new byte[4096];
        while (!sb.ToString().Contains("<EOF>"))
        {
            int n = s.Read(buf); if (n <= 0) break;
            sb.Append(Encoding.UTF8.GetString(buf, 0, n));
        }
        return sb.ToString().Split("<EOF>")[0];
    }

    public async Task SnapshotAsync(string file)
    {
        var bytes = await Http.GetByteArrayAsync($"http://{host}:8080/snapshot.jpg");
        await File.WriteAllBytesAsync(file, bytes);
    }

    public async Task DoAsync(string actie, double seconds)
    {
        var (cmd, min, max) = actie switch
        {
            "draai_links" => ("move 17", 1.0, 3.0),
            "draai_rechts" => ("move 13", 1.0, 3.0),
            "vooruit" => ("move 11", 1.0, 4.0),
            "achteruit" => ("move 15", 1.0, 3.0),
            _ => ("move 10", 0.0, 0.0),
        };
        if (cmd == "move 10") return;
        seconds = Math.Clamp(seconds, min, max);
        Send(cmd);
        try { await Task.Delay(TimeSpan.FromSeconds(seconds)); }
        finally
        {
            if (!TryStop() && !TryStop()) throw new IOException("stop-commando kwam niet aan");
        }
        await Task.Delay(3500);          // let the legs settle so the next photo is sharp
    }
}

/// <summary>Dutch text-to-speech with Piper, played through the default sound device.</summary>
class Speaker(string tools)
{
    readonly string piper = Path.Combine(tools, "piper", "piper.exe");
    readonly string voice = Path.Combine(tools, "voices", "nl_NL-ronnie-medium.onnx");
    readonly SemaphoreSlim one = new(1, 1);

    [DllImport("winmm.dll", CharSet = CharSet.Unicode)]
    static extern bool PlaySound(string file, IntPtr module, uint flags);
    const uint SND_SYNC = 0x0000, SND_FILENAME = 0x20000, SND_NODEFAULT = 0x0002;

    public async Task SayAsync(string text)
    {
        if (string.IsNullOrWhiteSpace(text)) return;
        await one.WaitAsync();
        try
        {
            var wav = Path.Combine(Path.GetTempPath(), $"spin-{Guid.NewGuid():N}.wav");
            var psi = new ProcessStartInfo(piper)
            {
                RedirectStandardInput = true, RedirectStandardError = true, RedirectStandardOutput = true,
                UseShellExecute = false, CreateNoWindow = true,
            };
            foreach (var a in new[] { "--model", voice, "--output_file", wav }) psi.ArgumentList.Add(a);
            using (var p = Process.Start(psi)!)
            {
                var utf8 = new StreamWriter(p.StandardInput.BaseStream, new UTF8Encoding(false));
                await utf8.WriteAsync(text); await utf8.FlushAsync(); p.StandardInput.Close();
                _ = p.StandardError.ReadToEndAsync(); _ = p.StandardOutput.ReadToEndAsync();
                await p.WaitForExitAsync();
            }
            if (File.Exists(wav))
            {
                await Task.Run(() => PlaySound(wav, IntPtr.Zero, SND_FILENAME | SND_SYNC | SND_NODEFAULT));
                try { File.Delete(wav); } catch { }
            }
        }
        catch (Exception e) { Program.Info("  (spraak mislukt: " + e.Message + ")", ConsoleColor.DarkYellow); }
        finally { one.Release(); }
    }
}
