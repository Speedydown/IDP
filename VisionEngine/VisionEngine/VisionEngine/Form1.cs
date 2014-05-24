using JL_VisionLib_V3;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using VisionEngine.Network;

namespace VisionEngine
{
    public partial class Form1 : Form
    {
        private NetworkInterface networkInterface;
        private NetworkBuffer buffer;
        VisionEngine.VisionLabInterface.VisionLabInterface vi;

        public Form1()
        {
            InitializeComponent(); 
            CmdInt.Init();
            vi = new VisionEngine.VisionLabInterface.VisionLabInterface();

            this.buffer = new NetworkBuffer();
            this.networkInterface = new NetworkInterface(this.buffer);
        }

        private void GetAPicture()
        {
            pictureBoxInput.SizeMode = PictureBoxSizeMode.StretchImage;
            pictureBoxOutput.SizeMode = PictureBoxSizeMode.StretchImage;

            while (true)
            {
                this.Refresh();
                Thread.Sleep(100);

                networkInterface.Send("gimg<EOF>");
                networkInterface.Recv();
                string test = buffer.Get();


                byte[] bytes = Convert.FromBase64String(test);

                Image image;
                using (MemoryStream ms = new MemoryStream(bytes))
                {
                    image = Image.FromStream(ms);
                    pictureBoxInput.Image = image;
                    this.pictureBoxOutput.Image = vi.processImage(new Bitmap(image));
                    image.Save("Image.jpg", System.Drawing.Imaging.ImageFormat.Jpeg);
                }
            }

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void StartButton_Click(object sender, EventArgs e)
        {
            GetAPicture();
        }


    }
}
