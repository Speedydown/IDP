using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SharpDX.DirectInput;
using System.Threading;

namespace VisionEngine
{
    public class GameControllerHandler
    {
        private CommandHandler chandler;
        private Thread controllerThread;
        private Semaphore controllerSemaphore;

        // joystick joystick
        private Joystick joystick;
        // joystick
        private int move;
        // dpad
        private int hwchange;
        // buttons
        private int buttons;

        // send string
        private string sendcmd;
        private string btncmd;
        private string dpdcmd;

        // help for input updates
        private float sec = DateTime.Now.Second;
        private string oldjoycmd = "";
        private string oldbtncmd = "";
        private string olddpdcmd = "";


        public GameControllerHandler(CommandHandler chandler)
        {
            this.chandler = chandler;
            this.controllerSemaphore = new Semaphore(1,1);

        }

        public void enable()
        {
            // Initialize DirectInput
            var directInput = new DirectInput();

            // Find a Gamepad Guid
            var gamepadGuid = Guid.Empty;

            DeviceType[] dtList = { DeviceType.Gamepad, DeviceType.Joystick, DeviceType.FirstPerson };
            IList<DeviceInstance> deviceInstanceList = null;

            foreach (DeviceType dt in dtList)
            {
                deviceInstanceList = directInput.GetDevices(dt, DeviceEnumerationFlags.AllDevices);

                if (deviceInstanceList.Count > 0)
                {
                    break;
                }
            }



            foreach (var deviceInstance in deviceInstanceList)
                gamepadGuid = deviceInstance.InstanceGuid;

            // If Gamepad not found, throws an error
            if (gamepadGuid == Guid.Empty)
            {
                Console.WriteLine("No gamepad found.");
            }

            // Instantiate the gamepad

            joystick = null;

            try
            {
                joystick = new Joystick(directInput, gamepadGuid);
            }
            catch (Exception)
            {
                this.disable();
                return;
            }

            Console.WriteLine("Found Joystick/Gamepad with GUID: {0}", gamepadGuid);

            // Query all suported ForceFeedback effects
            var allEffects = joystick.GetEffects();
            foreach (var effectInfo in allEffects)
                Console.WriteLine("Effect available {0}", effectInfo.Name);

            // Set BufferSize in order to use buffered data.
            joystick.Properties.BufferSize = 128;

            // Acquire the joystick
            joystick.Acquire();


            controllerThread = new Thread(() => run());
            controllerThread.Start();
        }

        public void disable()
        {
            controllerSemaphore.WaitOne();
            if (controllerThread != null)
            {
                controllerThread.Abort();
            }
            controllerSemaphore.Release();
        }

        public void run()
        {
            while (true)
            {
                controllerSemaphore.WaitOne();

                #region Left Joystick
                //STOP
                if (getCurrentState().X > 25000 && getCurrentState().X < 40000 && getCurrentState().Y > 25000 && getCurrentState().Y < 40000)
                {
                    move = 10;
                }

                //LEFTFORWARD
                if (getCurrentState().X < 20000 && getCurrentState().Y < 25000)
                {
                    move = 18;
                }

                //FORWARD
                if (getCurrentState().Y < 20000 && getCurrentState().X > 25000 && getCurrentState().X < 35000)
                {
                    move = 11;
                }

                //RIGHTFORWARD
                if (getCurrentState().X > 45000 && getCurrentState().Y < 25000)
                {
                    move = 12;
                }

                //RIGHT
                if (getCurrentState().X > 45000 && getCurrentState().Y > 25000 && getCurrentState().Y < 35000)
                {
                    move = 13;
                }

                //RIGHTDOWN
                if (getCurrentState().X > 40000 && getCurrentState().Y > 45000)
                {
                    move = 14;
                }

                //DOWN
                if (getCurrentState().Y > 45000 && getCurrentState().X > 20000 && getCurrentState().X < 45000)
                {
                    move = 15;
                }

                //LEFTDOWN
                if (getCurrentState().X < 20000 && getCurrentState().Y > 40000)
                {
                    move = 16;
                }

                //LEFT
                if (getCurrentState().X < 20000 && getCurrentState().Y > 25000 && getCurrentState().Y < 35000)
                {
                    move = 17;
                }

                #endregion

                #region DPAD

                if (getCurrentState().PointOfViewControllers[0] == 0)
                {
                    hwchange = 1;
                }

                if (getCurrentState().PointOfViewControllers[0] == 9000)
                {
                    hwchange = 2;
                }

                if (getCurrentState().PointOfViewControllers[0] == 18000)
                {
                    hwchange = 3;
                }

                if (getCurrentState().PointOfViewControllers[0] == 27000)
                {
                    hwchange = 4;
                }

                if (getCurrentState().PointOfViewControllers[0] == -1)
                {
                    hwchange = 0;
                }

                #endregion

                #region Buttons

                if (getCurrentState().Buttons[0] == true)
                {
                    buttons = 1;
                }

                if (getCurrentState().Buttons[1] == true)
                {
                    buttons = 2;
                }

                if (getCurrentState().Buttons[2] == true)
                {
                    buttons = 3;
                }

                if (getCurrentState().Buttons[3] == true)
                {
                    buttons = 4;
                }

                if (getCurrentState().Buttons[4] == true)
                {
                    buttons = 5;
                }

                if (getCurrentState().Buttons[5] == true)
                {
                    buttons = 6;
                }

                if (getCurrentState().Buttons[10] == true)
                {
                    if (sec != DateTime.Now.Second)
                    {
                        sendCommand("horn");
                        sec = DateTime.Now.Second;
                    }
                }
                #endregion

                #region Get and Send Input
                getInputJoyStick(move);
                getInputDpad(hwchange);
                getInputButton(buttons);

                if (sec != (DateTime.Now.Second / 2) && sendcmd != oldjoycmd)
                {
                    sendCommand(sendcmd);

                    sec = DateTime.Now.Second;

                    oldjoycmd = sendcmd;
                }

                if (sec != (DateTime.Now.Second / 2) && dpdcmd != olddpdcmd)
                {
                    sendCommand(dpdcmd);

                    sec = DateTime.Now.Second;

                    olddpdcmd = dpdcmd;
                }

                if (sec != (DateTime.Now.Second / 2) && btncmd != oldbtncmd)
                {
                    sendCommand(btncmd);

                    sec = DateTime.Now.Second;

                    oldbtncmd = btncmd;
                }

                #endregion

                controllerSemaphore.Release();
                Thread.Sleep(1);
            }
        }

        public void getInputJoyStick(int moveInt)
        {
            switch (moveInt)
            {
                // stop
                case 10:
                    getJoystick("move " + moveInt.ToString());
                    break;
                // fw
                case 11:
                    getJoystick("move " + moveInt.ToString());
                    break;
                // rfw
                case 12:
                    getJoystick("move " + moveInt.ToString());
                    break;
                // r
                case 13:
                    getJoystick("move " + moveInt.ToString());
                    break;
                // rbw
                case 14:
                    getJoystick("move " + moveInt.ToString());
                    break;
                // bw
                case 15:
                    getJoystick("move " + moveInt.ToString());
                    break;
                // lbw
                case 16:
                    getJoystick("move " + moveInt.ToString());
                    break;
                // l
                case 17:
                    getJoystick("move " + moveInt.ToString());
                    break;
                //lfw
                case 18:
                    getJoystick("move " + moveInt.ToString());
                    break;
                default:
                    break;
            }
        }

        public void getInputDpad(int mod)
        {
            switch (mod)
            {
                case 1:
                    getDpad("dpup");
                    break;
                case 2:
                    getDpad("dpri");
                    break;
                case 3:
                    getDpad("dpdn");
                    break;
                case 4:
                    getDpad("dple");
                    break;
                default:
                    break;
            }
        }

        public void getInputButton(int keys)
        {
            switch (keys)
            {
                case 1:
                    getButtons("btns");
                    break;
                case 2:
                    getButtons("btnx");
                    break;
                case 3:
                    getButtons("btno");
                    break;
                case 4:
                    getButtons("btnt");
                    break;
                case 5:
                    getButtons("move 20");
                    break;
                case 6:
                    getButtons("move 21");
                    break;
                default:
                    break;
            }
        }

        public void getJoystick(string command)
        {
            sendcmd = command;
        }

        public void getButtons(string command)
        {
            btncmd = command;
        }

        public void getDpad(string command)
        {
            dpdcmd = command;
        }

        public void sendCommand(string send)
        {
            chandler.execute(send);
            Console.WriteLine(send);
        }

        public JoystickState getCurrentState()
        {
            try
            {

                return joystick.GetCurrentState();
            }
            catch (Exception e)
            {
                this.disable();
                return null;
            }
        }


    }
}
