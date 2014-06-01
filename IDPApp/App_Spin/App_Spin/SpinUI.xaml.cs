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



// The Blank Page item template is documented at http://go.microsoft.com/fwlink/?LinkId=234238

namespace App_Spin
{
    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class SpinUI : Page
    {
        private int battery;
        private int slope;

        public string move = "";
                       
        public SpinUI()
        {
            this.InitializeComponent();
            
            var timer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(1) };
            timer.Tick += (o, e) => lblHour.Text = DateTime.Now.Hour.ToString();
            timer.Tick += (o, e) => lblMin.Text = DateTime.Now.Minute.ToString();
            timer.Tick += (o, e) => lblSec.Text = DateTime.Now.Second.ToString();
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
            #endregion
            
            getBattery();
            getSlope();
        }

        private void getBattery()
        {
            battery = 100;
            lblBattery.Text = "Battery: " + battery.ToString();
        }

        private void getSlope()
        {
            slope = 50;
            lblSlope.Text = "Slope: " + slope.ToString();
        }

        
        private async void sendCmd(string moveMessage)
        {
            /* Send msg method to Raspberry Pi
             * Needs input string (move)
             */

            //await (Network.NetworkHandler.Send(moveMessage));

            //if (cmdSending == false)
            //{

            //    cmdSending = true;

            //    await (Network.NetworkHandler.Send(moveMessage));
            //    await (Network.NetworkHandler.Recv());

            //    cmdSending = false;

            //    Network.NetworkHandler.InputBuffer.Get();
            //}

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
            getBattery();
            getSlope();
        }

        // LF - FW - RF

        #region Left-Fw

        private void btnLeftFw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 18";
            sendCmd(move);
        }

        private void btnLeftFw_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        #region Forward

        private void btnFw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 11";
            sendCmd(move);
        }

        private void btnFw_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        #region Right-Fw

        private void btnRightFw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 12";
            sendCmd(move);
        }

        private void btnRightFw_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        // L - R

        #region Left

        private void btnLeft_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 17";
            sendCmd(move);
        }

        private void btnLeft_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        #region Right

        private void btnRight_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 13";
            sendCmd(move);
        }

        private void btnRight_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        //LB - BW - RB

        #region Left-Bw

        private void btnLeftBw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 16";
            sendCmd(move);
        }

        private void btnLeftBw_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        #region Backward

        private void btnBw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 15";
            sendCmd(move);
        }

        private void btnBw_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

        #region Right-Bw

        private void btnRightBw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 14";
            sendCmd(move);
        }

        private void btnRightBw_Released(object sender, PointerRoutedEventArgs e)
        {
            stop();
        }

        #endregion

    }
}
