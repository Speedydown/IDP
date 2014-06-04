using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.UI.Input;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;

/* CONTROLLER */
using Windows.Devices.Enumeration;
using Windows.Devices.Bluetooth;
using Windows.Devices.Bluetooth.Rfcomm;
using Windows.Devices.Bluetooth.GenericAttributeProfile;

using Windows.Devices.HumanInterfaceDevice;
using Windows.Storage;
using Windows.Storage.Streams;


// The Blank Page item template is documented at http://go.microsoft.com/fwlink/?LinkId=234238

namespace App_Spin
{
    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class SpinUI : Page
    {
        /*BATTERY AND SLOPE INTS*/
        private int battery;
        private int slope;
        /*MOVE STRING*/
        public string move = "";
        /*bool to check sending*/
        public bool sending = false;

        public SpinUI()
        {
            this.InitializeComponent();
            
            /* TIMER IN RIGHT TOP CORNER SPLIT IN HOUR MINUTE SECOND */
            var timer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(1) };
            timer.Tick += (o, e) => lblHour.Text = "H " + DateTime.Now.Hour.ToString();
            timer.Tick += (o, e) => lblMin.Text = "M " + DateTime.Now.Minute.ToString();
            timer.Tick += (o, e) => lblSec.Text = "S " + DateTime.Now.Second.ToString();
            timer.Start();

            /*Human Interface Device, DualShock 4*/

            /*
             * Add new EventHandlers per button, not standard supported.
             * Each button will get two new handlers, *_Pressed and *_Released.
             */

            #region Handlers
            //LF
            btnLeftFw.AddHandler(PointerPressedEvent, new PointerEventHandler(btnLeftFw_Pressed), true);
            btnLeftFw.AddHandler(PointerReleasedEvent, new PointerEventHandler(btnLeftFw_Released), true);
            //FW
            btnFw.AddHandler(PointerPressedEvent, new PointerEventHandler(btnFw_Pressed), true);
            btnFw.AddHandler(PointerReleasedEvent, new PointerEventHandler(btnFw_Released), true);
            //RF
            btnRightFw.AddHandler(PointerPressedEvent, new PointerEventHandler(btnRightFw_Pressed), true);
            btnRightFw.AddHandler(PointerReleasedEvent, new PointerEventHandler(btnRightFw_Released), true);
            //LEFT
            btnLeft.AddHandler(PointerPressedEvent, new PointerEventHandler(btnLeft_Pressed), true);
            btnLeft.AddHandler(PointerReleasedEvent, new PointerEventHandler(btnLeft_Released), true);
            //RIGHT
            btnRight.AddHandler(PointerPressedEvent, new PointerEventHandler(btnRight_Pressed), true);
            btnRight.AddHandler(PointerReleasedEvent, new PointerEventHandler(btnRight_Released), true);
            //LB
            btnLeftBw.AddHandler(PointerPressedEvent, new PointerEventHandler(btnLeftBw_Pressed), true);
            btnLeftBw.AddHandler(PointerReleasedEvent, new PointerEventHandler(btnLeftBw_Released), true);
            //BW
            btnBw.AddHandler(PointerPressedEvent, new PointerEventHandler(btnBw_Pressed), true);
            btnBw.AddHandler(PointerReleasedEvent, new PointerEventHandler(btnBw_Released), true);
            //RB
            btnRightBw.AddHandler(PointerPressedEvent, new PointerEventHandler(btnRightBw_Pressed), true);
            btnRightBw.AddHandler(PointerReleasedEvent, new PointerEventHandler(btnRightBw_Released), true);

            //ConnectDS
            btnConnDS.AddHandler(PointerPressedEvent, new PointerEventHandler(btnConnDS_Pressed), true);

            //lblBattery
            //lblSlope
            lblBattery.AddHandler(PointerPressedEvent, new PointerEventHandler(lblBattery_Pressed), true);
            lblSlope.AddHandler(PointerPressedEvent, new PointerEventHandler(lblSlope_Pressed), true);
            #endregion
            
            getBattery();
            getSlope();
        }

        /*IDs FOR THE WIRELESS CONTROLLER (HID DEVICE)*/
        UInt16 PID = 0x05C4; // product ID
        UInt16 VID = 0x054C; // vendor ID
        UInt16 usagePage = 0x01; // usagePage
        UInt16 UID = 0x05; // usage ID

        HidDevice ds4;

        private async void ds4detect()
        {
            string select = HidDevice.GetDeviceSelector(usagePage, UID, VID, PID);
            var devices = await DeviceInformation.FindAllAsync(select);

            if (devices.Count > 0)
            {
                /*
                 * SCAN FOR HID DEVICES
                 * ElementAt(0) --> ds4
                 */
                ds4 = await HidDevice.FromIdAsync(devices.ElementAt(0).Id, FileAccessMode.ReadWrite);
                txtTest.Text = devices.ElementAt(0).Id.ToString();
                // returns
                // \\?\HID#{00001124-0000-1000-8000-00805f9b34fb}_VID&0002054c_PID&05c4#9&1d5c15b1&4&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}
                //ds4 = HidDevice(devices.ElementAt(0).Id);
                
                /*TEST SECTION*/
                if (ds4 != null)
                    txtTest.Text = "DS4 Found!";
                
                if (ds4 == null)
                    txtTest.Text = "DS4 NOT found!";
            }
            else
            {
                txtJoytest.Text = "No devices found!";
            }
        }

        private async void getBattery()
        {
        //    await (Network.NetworkHandler.Send("gbat"));
        //    await (Network.NetworkHandler.Recv());
        //    battery = Convert.ToInt16(Network.NetworkHandler.InputBuffer.Get());

            /*TEST*/
            battery = 100;

            //LABEL
            lblBattery.Text = "Battery: " + battery.ToString();
        }

        private async void getSlope()
        {
            //await (Network.NetworkHandler.Send("gslo"));
            //await (Network.NetworkHandler.Recv());
            //slope = Convert.ToInt16(Network.NetworkHandler.InputBuffer.Get());

            /*TEST*/
            slope = 50;

            //LABEL
            lblSlope.Text = "Slope: " + slope.ToString();
        }
        
        private async void sendCmd(string moveMessage)
        {
            /* Send msg method to Raspberry Pi
             * Needs input string (move)
             */

            if (sending == false)
            {
                sending = true;

                await (Network.NetworkHandler.Send(moveMessage));
                await (Network.NetworkHandler.Recv());

                sending = false;

                Network.NetworkHandler.InputBuffer.Get();
            }
            txtJoytest.Text = moveMessage;
        }

        /* Bindings 
         *  for buttons to send move commands to Raspberry Pi
         *  move commands are as follows:
         *      - move 11-18 ; move in 8 directions, 11 is forward, clockwise to 18 is left-forward
         *      - move 10    ; to stop current movement
         */

        /* Stop command for move */
        private void stop()
        {
            move = "move 10";
            sendCmd(move);
        }

        // LF - FW - RF

        #region Left-Fw
        // Move left-forward
        private void btnLeftFw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 18";
            sendCmd(move);
        }

        // Stop movement
        private void btnLeftFw_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        #region Forward
        // Move forward
        private void btnFw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 11";
            sendCmd(move);
        }

        // Stop movement
        private void btnFw_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        #region Right-Fw
        // Move right-forward
        private void btnRightFw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 12";
            sendCmd(move);
        }

        // Stop movement
        private void btnRightFw_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        // L - R

        #region Left
        // Move left
        private void btnLeft_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 17";
            sendCmd(move);
        }

        // Stop movement
        private void btnLeft_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        #region Right
        // Move right
        private void btnRight_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 13";
            sendCmd(move);
        }

        // Stop movement
        private void btnRight_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        //LB - BW - RB

        #region Left-Bw
        // Move left-backwards
        private void btnLeftBw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 16";
            sendCmd(move);
        }

        // Stop movement
        private void btnLeftBw_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        #region Backward
        // Move backwards
        private void btnBw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 15";
            sendCmd(move);
        }

        // Stop movement
        private void btnBw_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        #region Right-Bw
        // Move right-backwards
        private void btnRightBw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 14";
            sendCmd(move);
        }

        // Stop movement
        private void btnRightBw_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        private void btnConnDS_Pressed(object sender, PointerRoutedEventArgs e)
        {
            ds4detect();
        }

        private void lblBattery_Pressed(object sender, PointerRoutedEventArgs e)
        {
            
            if (popBattery.IsOpen == false)
            {
                popBattery.IsOpen = true;
                txtTest.Text = "battery pressed";
            }
            else
            {
                popBattery.IsOpen = false;
                txtTest.Text = "popup closed";
            }
        }

        private void lblSlope_Pressed(object sender, PointerRoutedEventArgs e)
        {

        }
    }
}
