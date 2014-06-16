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

namespace App_Spin
{
    /// <summary>
    /// SpinUI: The UI page for controlling the Spider
    /// </summary>
    public sealed partial class SpinUI : Page
    {
        /*BATTERY AND SLOPE INTS*/
        private int battery;
        private int slope;
        /*MOVE STRING*/
        public string move = "";
        /*BOOL TO CHECK SENDING*/
        public bool sending = false;

        /*VALUES FOR SLIDERS SPEED AND HEIGHT*/
        private int heightValue;
        private int speedValue;

        public Image image;

        public SpinUI()
        {
            this.InitializeComponent();
            
            /* TIMER IN RIGHT TOP CORNER SPLIT IN HOUR MINUTE SECOND */
            var timer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(1) };
            timer.Tick += (o, e) => lblHour.Text = "H " + DateTime.Now.Hour.ToString();
            timer.Tick += (o, e) => lblMin.Text = "M " + DateTime.Now.Minute.ToString();
            timer.Tick += (o, e) => lblSec.Text = "S " + DateTime.Now.Second.ToString();
            timer.Start();
            
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
            
            //lblBattery
            //lblSlope
            lblBattery.AddHandler(PointerPressedEvent, new PointerEventHandler(lblBattery_Pressed), true);
            lblSlope.AddHandler(PointerPressedEvent, new PointerEventHandler(lblSlope_Pressed), true);
            #endregion
                        
            getBattery();
            getSlope();
            sldHeight.ValueChanged += sldHeight_ValueChanged;
            sldSpeed.ValueChanged += sldSpeed_ValueChanged;
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

        //private async void getImage()
        //{
        //    if (sending == false)
        //    {
        //        sending = true;

        //        await (Network.NetworkHandler.Send("gifm"));
        //        await (Network.NetworkHandler.Recv());

        //        sending = false;
        //    }

        //    byte[] bytes = Convert.FromBase64String(Network.NetworkHandler.InputBuffer.Get());
        //    using (var ms = new MemoryStream())
        //    {  
        //        using (var imageFile = new StreamWriter(ms)
        //        {
        //            imageFile.Write(bytes, 0, bytes.Length);
        //            imageFile.Flush();
        //        }
        //    }
        //}

        private async void sendCmd(string moveMessage)
        {
            /* Send msg method to Raspberry Pi
             * Needs input string (move)
             */

            //if (sending == false)
            //{
            //    sending = true;

            //    await (Network.NetworkHandler.Send(moveMessage));
            //    await (Network.NetworkHandler.Recv());

            //    sending = false;

            //    Network.NetworkHandler.InputBuffer.Get();
            //}
            txtJoytest.Text = moveMessage;
        }

        /* Joypad Bindings 
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


        // label Battery Pressed to open batterygraph
        private void lblBattery_Pressed(object sender, PointerRoutedEventArgs e)
        {
            
            if (popBattery.IsOpen == false)
            {
                popBattery.IsOpen = true;
            }
            else
            {
                popBattery.IsOpen = false;
            }
        }

        // label Slope Pressed to open slopegraph
        private void lblSlope_Pressed(object sender, PointerRoutedEventArgs e)
        {

        }

        // Return to MainPage
        private void btnReturn_Click(object sender, RoutedEventArgs e)
        {
            this.Frame.Navigate(typeof(MainPage));
        }

        // Slider for configuring spider height on the fly
        private void sldHeight_ValueChanged(object sender, RangeBaseValueChangedEventArgs e)
        {
            heightValue = Convert.ToInt16(sldHeight.Value);

            /*INSERT NETWORK COMMAND*/
        }

        // Slider for configuring spider speed on the fly
        private void sldSpeed_ValueChanged(object sender, RangeBaseValueChangedEventArgs e)
        {
            speedValue = Convert.ToInt16(sldSpeed.Value);

            /*INSERT NETWORK COMMAND*/
        }
    }
}
