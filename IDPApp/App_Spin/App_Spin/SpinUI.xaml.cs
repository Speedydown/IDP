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
        private bool joyDown = false;
        private Point joyStart = new Point(-350,-350);
        private Thickness m;

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

        private void cmd_goJoystick_Click(object sender, RoutedEventArgs e)
        {
            //this.Frame.Navigate(typeof(JoystickTest));
        }

        private void joyPressed(object sender, PointerRoutedEventArgs e)
        {
            joyDown = true;
        }

        private void joyReleased(object sender, PointerRoutedEventArgs e)
        {
            joyDown = false;
        }

        private void joyMoved(object sender, PointerRoutedEventArgs e)
        {
            if (joyDown == true)
            {
                GeneralTransform gt = TransformToVisual(joyStick);
                Point screenPoint;

                screenPoint = gt.TransformPoint(new Point(screenPoint.X, screenPoint.Y));

                txtJoytest.Text = screenPoint.ToString();
                
                //p = e.GetCurrentPoint(joyStick);

                
                m = joyStick.Margin;
                m.Left = screenPoint.X;
                m.Top = screenPoint.Y;

                joyStick.Margin = m;
            }
        }
    }
}
