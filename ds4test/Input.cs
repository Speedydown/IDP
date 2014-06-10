using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using SharpDX.DirectInput;

namespace ds4test
{
    class Input
    {
        #region Variables
        // joystick joystick
        Joystick joystick;
        
        // joystick
        int move;
        // dpad
        int hwchange;
        // buttons
        int buttons;

        // send string
        string sendcmd;
        string btncmd;
        string dpdcmd;

        // help for input updates
        float sec = DateTime.Now.Second;
        string oldjoycmd = "";
        string oldbtncmd = "";
        string olddpdcmd = "";
        #endregion

        public void initDS4()
        {
            // Initialize DirectInput
            var directInput = new DirectInput();

            // Find a Gamepad Guid
            var gamepadGuid = Guid.Empty;

            //PC Depended : DeviceType = Device op laptop, PC is Device. Vaag
            foreach (var deviceInstance in directInput.GetDevices(DeviceType.FirstPerson, DeviceEnumerationFlags.AllDevices))
                gamepadGuid = deviceInstance.InstanceGuid;

            // If Gamepad not found, throws an error
            if (gamepadGuid == Guid.Empty)
            {
                Console.WriteLine("No gamepad found.");
                Console.ReadKey();
                Environment.Exit(1);
            }

            // Instantiate the gamepad
            joystick = new Joystick(directInput, gamepadGuid);

            Console.WriteLine("Found Joystick/Gamepad with GUID: {0}", gamepadGuid);

            // Query all suported ForceFeedback effects
            var allEffects = joystick.GetEffects();
            foreach (var effectInfo in allEffects)
                Console.WriteLine("Effect available {0}", effectInfo.Name);

            // Set BufferSize in order to use buffered data.
            joystick.Properties.BufferSize = 128;

            // Acquire the joystick
            joystick.Acquire();

            while (true)
            {
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
                if (getCurrentState().X > 45000 && getCurrentState().Y > 45000)
                {
                    move = 14;
                }

                //DOWN
                if (getCurrentState().Y > 45000 && getCurrentState().X > 25000 && getCurrentState().X < 35000)
                {
                    move = 15;
                }

                //LEFTDOWN
                if (getCurrentState().X < 20000 && getCurrentState().Y > 45000)
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
            Console.WriteLine(send);
        }

        public JoystickState getCurrentState()
        {
            return joystick.GetCurrentState();
        }
    }
}
