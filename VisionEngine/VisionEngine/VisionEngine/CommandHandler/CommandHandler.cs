using JL_VisionLib_V3;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using VisionEngine.Network;
using VisionEngine.VisionInterface;

namespace VisionEngine
{
    public class CommandHandler
    {
        private NetworkInterface networkInterface;
        private VisionLabInterface visionLabInterface;
        private Thread streamThread;
        private VisionEngineForm visionEngine;
        private Semaphore commandHandlerSemaphore;
        private ConnectionForm connectionForm;

        public CommandHandler(NetworkInterface networkInterface, ConnectionForm connectionForm)
        {
            CmdInt.Init();
            this.connectionForm = connectionForm;
            this.networkInterface = networkInterface;
            this.visionLabInterface = new VisionLabInterface();
            this.visionEngine = new VisionEngineForm(this, connectionForm);
            this.commandHandlerSemaphore = new Semaphore(1, 1);
            this.visionEngine.Show();
        }

        public void startStream()
        {
            streamThread = new Thread(() => CommandHandler.runStream(this, visionLabInterface, visionEngine));
            streamThread.Start();
        }

        public void stopStream()
        {
            commandHandlerSemaphore.WaitOne();
            if (streamThread != null)
            {
                streamThread.Abort();
            }
            commandHandlerSemaphore.Release(); 
        }

        public void disconnect()
        {
            networkInterface.Disconnect();
            connectionForm.UpdateFormAFterConnect("Disconnected");
        }

        public string execute(string Command)
        {
            commandHandlerSemaphore.WaitOne();
            networkInterface.Send(Command + "<EOF>");
            string output = networkInterface.Recv();
            commandHandlerSemaphore.Release();
            return output;
            
        }

        public static void runStream(CommandHandler commandHandler, VisionLabInterface visionLabInterface, VisionEngineForm visionEngine)
        {
            while (true)
            {
                byte[] bytes = Convert.FromBase64String(commandHandler.execute("gimg"));

                Image InputImage;
                Image OutputImage;
                using (MemoryStream ms = new MemoryStream(bytes))
                {
                    try
                    {
                        InputImage = Image.FromStream(ms);
                        OutputImage = visionLabInterface.processImage(new Bitmap(InputImage));
                        visionEngine.Invoke(visionEngine.UpdateImageDelegate, new Object[] { InputImage, OutputImage });
                        Thread.Sleep(100);
                        OutputImage.Save("imageo.jpg", System.Drawing.Imaging.ImageFormat.Jpeg);
                        InputImage.Save("imagei.jpg", System.Drawing.Imaging.ImageFormat.Jpeg);
                        Thread.Sleep(100);
                    }
                    catch (Exception)
                    {

                    }
                }
            }
        }

    }
}
