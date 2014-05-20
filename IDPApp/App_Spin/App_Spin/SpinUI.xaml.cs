using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
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
        PointerPoint pPoint;
        Point screenPoint;

        private bool grdPress = false;
        public string move = "";

        public SpinUI()
        {
            this.InitializeComponent();
        }

        private void AppBarButton_Click(object sender, RoutedEventArgs e)
        {
            this.Frame.Navigate(typeof(MainPage));
        }

        private void Pressed(object sender, PointerRoutedEventArgs e)
        {

        }

        private void cmd_joyTest_Click(object sender, RoutedEventArgs e)
        {
            //TODO button
        }

        private void grdReleased(object sender, PointerRoutedEventArgs e)
        {
            grdPress = false;

            Thickness n = joyStick.Margin;
            n.Left = 150;
            n.Top = 150;

            joyStick.Margin = n;
        }

        private async void grdPressed(object sender, PointerRoutedEventArgs e)
        {
            pPoint = e.GetCurrentPoint(joyStick);
            screenPoint = pPoint.Position;

            Thickness m = joyStick.Margin;
                
            //if (screenPoint.X )
            m.Left = screenPoint.X + 50;
            m.Top = screenPoint.Y + 50;

            joyStick.Margin = m;

            txtJoytest.Text = "X" + screenPoint.X.ToString() + "Y" + screenPoint.Y.ToString();

            grdPress = true;

            if (screenPoint.X < 0)
            {
                if (screenPoint.Y < 0) /*LINKS*/
                {
                    //move = "tsen 30";
                    //await (Network.NetworkHandler.Send(move));
                    //await (Network.NetworkHandler.Recv());
                    //Network.NetworkHandler.InputBuffer.Get();
                }
                else /*screenPoint.Y > 0 == DOWN */
                {

                }
            }
            else /*screenPoint.X > 0*/
            {
                if (screenPoint.Y < 0) /*UP*/
                {

                }
                else /*screenPoint.Y > 0 == RECHTS*/
                {

                }
            }

            
            

            //txtJoytest.Text = screenPoint.ToString();
        }

        private async void Button_Click(object sender, RoutedEventArgs e)
        {
            //move = "tsen 30";
            //await (Network.NetworkHandler.Send(move));
            //await (Network.NetworkHandler.Recv());
            //Network.NetworkHandler.InputBuffer.Get();
        }
    }
}
