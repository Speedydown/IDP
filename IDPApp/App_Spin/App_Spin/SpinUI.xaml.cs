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
        //PointerPoint pPoint;
        //Point screenPoint;

        //private bool grdPress = false;
        public string move = "";
        public int count = 0;

        public SpinUI()
        {
            this.InitializeComponent();
            /*
             * Add new EventHandlers per button, not standard supported.
             * Each button will get two new handlers, *_Pressed and *_Released.
             */
            // btnFw
            btnFw.AddHandler(PointerPressedEvent, new PointerEventHandler(btnFw_Pressed), true);
            btnFw.AddHandler(PointerReleasedEvent, new PointerEventHandler(btnFw_Released), true);
        }

        private void AppBarButton_Click(object sender, RoutedEventArgs e)
        {
            this.Frame.Navigate(typeof(MainPage));
        }

        private void Pressed(object sender, PointerRoutedEventArgs e)
        {

        }

        // LF - FW - RF

        #region Left-Fw

        #endregion

        #region Forward
        /*
         * Bindings for btnFw to send move commands to Raspberry Pi
         * move commands are as follows:
         * - move fw    ; to move forward
         * - move stop  ; to stop current movement
         */
        
        private void btnFw_Pressed(object sender, PointerRoutedEventArgs e)
        {
            move = "move 1";
            txtJoytest.Text = move;
        }

        private void btnFw_Released(object sender, PointerRoutedEventArgs e)
        {
            move = "move 0";
            txtJoytest.Text = move;
        }
        #endregion

        

        #region Right-Fw

        #endregion

        // L - R

        #region Left

        #endregion

        #region Right

        #endregion

        //LB - BW - RB

        #region Left-Bw

        #endregion

        #region Backward
        private void btnBw_Pressed(object sender, PointerRoutedEventArgs e)
        {

        }

        private void btnBw_Released(object sender, PointerRoutedEventArgs e)
        {

        }
        #endregion

        #region Right-Bw

        #endregion

    }
}
