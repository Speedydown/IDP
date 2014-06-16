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
        //private VisionLabInterface2 visionLabInterface;
        private BalloonFinder visionLabInterface;
        private Thread streamThread;
        private VisionEngineForm visionEngine;
        private Semaphore commandHandlerSemaphore;
        private ConnectionForm connectionForm;
        private GameControllerHandler gcHandler;
        //public static string input = "C:\\Users\\Miriam\\Desktop\\Input1.jpg";
        public CommandHandler(NetworkInterface networkInterface, ConnectionForm connectionForm)
        {
            CmdInt.Init();
            this.gcHandler = new GameControllerHandler(this);
            this.connectionForm = connectionForm;
            this.networkInterface = networkInterface;
            this.visionEngine = new VisionEngineForm(this, connectionForm, gcHandler);
            this.visionLabInterface = new BalloonFinder(this.visionEngine, this);
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

            /*if (Command == "gimg")
            {
                byte[] bytes = Convert.FromBase64String(output);

                Image InputImage;
                Image OutputImage;
                using (MemoryStream ms = new MemoryStream(bytes))
                {
                    try
                    {
                        InputImage = new Bitmap(Image.FromStream(ms));
                        OutputImage = visionLabInterface.processImage(new Bitmap(InputImage));
                        visionEngine.Invoke(visionEngine.UpdateImageDelegate, new Object[] { InputImage, InputImage });
                    }
                    catch (Exception)
                    {

                    }
                }
            }*/

            return output;

            
            
        }

        public static void runStream(CommandHandler commandHandler, BalloonFinder visionLabInterface, VisionEngineForm visionEngine)
        {
            while (true)
            {
                /*
                Image InputImage;
                Image OutputImage;
                InputImage = new Bitmap(Image.FromFile(CommandHandler.input));
                OutputImage = visionLabInterface.processImage(new Bitmap(InputImage));
                visionEngine.Invoke(visionEngine.UpdateImageDelegate, new Object[] { InputImage, OutputImage });*/
                
                byte[] bytes = Convert.FromBase64String(commandHandler.execute("gimg"));

                Image InputImage;
                Image OutputImage;
                using (MemoryStream ms = new MemoryStream(bytes))
                {
                    try
                    {
                        
                        InputImage = new Bitmap(Image.FromStream(ms));
                        //InputImage = new Bitmap(Image.FromFile("C:\\Users\\Miriam\\Desktop\\Input1.jpg"));
                        OutputImage = visionLabInterface.processImage(new Bitmap(InputImage));
                        visionEngine.Invoke(visionEngine.UpdateImageDelegate, new Object[] { InputImage, OutputImage });
                    }
                    catch (Exception)
                    {

                    }
                }
            }
        }

    }
}
