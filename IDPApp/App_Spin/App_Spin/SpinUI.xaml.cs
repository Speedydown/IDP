﻿using System;
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
        private int BatSlo;
        private int battery;
        private string slope;

        private int minute;

        /*MOVE STRING*/
        public string move = "";
        /*BOOL TO CHECK SENDING*/
        public bool sending = false;

        /*VALUES FOR SLIDERS SPEED AND HEIGHT*/
        private int heightValue;
        private int angleValue;

        private string modeselect = "smde 1";
        private Info i;

        public SpinUI()
        {
            this.i = new Info();
            if (i.getConnected() == true)
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

                cmbMissionSelect.SelectionChanged += cmbSelect_SelectionChanged;
                cmbMissionSelect.Items.Add("Handmatige besturing - Tablet");
                cmbMissionSelect.Items.Add("Handmatige besturing - Controller");
                cmbMissionSelect.Items.Add("Dansje");
                cmbMissionSelect.Items.Add("Spider Gap");
                cmbMissionSelect.Items.Add("Ballonnen");
                cmbMissionSelect.Items.Add("Teerballen");

                sldHeight.ValueChanged += sldHeight_ValueChanged;
                sldAngle.ValueChanged += sldAngle_ValueChanged;
                lblBattery.DataContextChanged += lblBattery_ContextChanged;
                lblSlope.DataContextChanged += lblSlope_ContextChanged;
            }
            else
            {
                this.Frame.Navigate(typeof(MainPage));
            }
        }

        private async void sendCmd(string message)
        {
            /* Send msg method to Raspberry Pi
             * Needs input string (move)
             */

            if (sending == false)
            {
                sending = true;

                await (Network.NetworkHandler.Send(message));
                await (Network.NetworkHandler.Recv());

                sending = false;

                if (message == "gbat" || message == "gslo")
                {
                    BatSlo = Convert.ToInt16(Network.NetworkHandler.InputBuffer.Get());
                }
                else
                {
                    Network.NetworkHandler.InputBuffer.Get();
                }

            }
        }

        #region Joystick Controls
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

        #endregion

        // label Battery Pressed to open batterygraph
        private void lblBattery_Pressed(object sender, PointerRoutedEventArgs e)
        {

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
        private async void sldHeight_ValueChanged(object sender, RangeBaseValueChangedEventArgs e)
        {
            heightValue = Convert.ToInt16(sldHeight.Value);

            sendCmd("shgt " + heightValue.ToString());
        }

        // Slider for configuring spider angle on the fly
        private async void sldAngle_ValueChanged(object sender, RangeBaseValueChangedEventArgs e)
        {
            angleValue = Convert.ToInt16(sldAngle.Value);

            sendCmd("sdeg " + angleValue.ToString());
        }

        /* Update info on status battery */
        private async void lblBattery_ContextChanged(FrameworkElement sender, DataContextChangedEventArgs args)
        {
            if (minute != DateTime.Now.Minute)
            {
                sendCmd("gbat");
                battery = BatSlo;

                //LABEL
                lblBattery.Text = "Battery: " + battery.ToString();
                minute = DateTime.Now.Minute;
            }
        }

        /* Update info on status slope */
        private async void lblSlope_ContextChanged(FrameworkElement sender, DataContextChangedEventArgs args)
        {
            sendCmd("gslo");
            slope = BatSlo.ToString();

            //LABEL
            lblSlope.Text = "Slope: " + slope.ToString();
        }

        private async void cmbSelect_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            /* Beide manuals zijn smde 1
             * Dansje is smde 2
             * Spider Gap is 3
             * Ballonnen is 4
             * Teerballen is 5
             */
            if (cmbMissionSelect.SelectedIndex == 0)
            {
                modeselect = "smde 1";
            }
            else
            {
                modeselect = "smde " + cmbMissionSelect.SelectedIndex.ToString();
            }
            sendCmd(modeselect);
        }
    }
}
