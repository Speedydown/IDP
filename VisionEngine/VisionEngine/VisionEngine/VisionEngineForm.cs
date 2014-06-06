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
using VisionEngine.VisionInterface;

namespace VisionEngine
{
    public partial class VisionEngineForm : Form
    {
        public delegate void UpdateImage(Bitmap Input, Bitmap Output);
        public UpdateImage UpdateImageDelegate;
        public delegate void UpdateImageBalloon(string color, int index);
        public UpdateImageBalloon UpdateImageBalloonDelegate;
        private CommandHandler commandHandler;
        private ConnectionForm connectionForm;
        private int ImageCount = 1;

        public VisionEngineForm(CommandHandler commandHandler, ConnectionForm connectionForm)
        {
            InitializeComponent();
            this.commandHandler = commandHandler;
            this.connectionForm = connectionForm;
            pictureBoxInput.SizeMode = PictureBoxSizeMode.StretchImage;
            pictureBoxOutput.SizeMode = PictureBoxSizeMode.StretchImage;
            UpdateImageDelegate = new UpdateImage(updateImages);
            UpdateImageBalloonDelegate = new UpdateImageBalloon(updateImageBalloon);
 
        }

        private void updateImageBalloon(string color, int index)
        {
            switch (color) { 
                case "RED":
                     PictureBox pb = (PictureBox) this.Controls.Find(("balloon" + index.ToString()), true)[0];
                     pb.Image = VisionEngine.Properties.Resources.balloonRed;
                    break;
                case "BLUE":
                     PictureBox pb1 = (PictureBox) this.Controls.Find(("balloon" + index.ToString()), true)[0];
                     pb1.Image = VisionEngine.Properties.Resources.balloonBlue;
                    break;
                case "GREEN":
                     PictureBox pb2 = (PictureBox) this.Controls.Find(("balloon" + index.ToString()), true)[0];
                     pb2.Image = VisionEngine.Properties.Resources.balloonGreen;
                    break;
    
            }
                
        }

        private void updateImages(Bitmap Input, Bitmap Output)
        {
            this.pictureBoxInput.Image = Input;
            this.pictureBoxOutput.Image = Output;
        }

        private void startStreamToolStripMenuItem_Click(object sender, EventArgs e)
        {
            commandHandler.startStream();
        }

        private void stopStreamToolStripMenuItem_Click(object sender, EventArgs e)
        {
            commandHandler.stopStream();
        }

        private void disconnectToolStripMenuItem_Click(object sender, EventArgs e)
        {
            commandHandler.disconnect();
            commandHandler.stopStream();
            connectionForm.Show();
            this.Dispose();
            
        }

        private void shutdownServerToolStripMenuItem_Click(object sender, EventArgs e)
        {
            commandHandler.execute("shtd");
            commandHandler.stopStream();
            connectionForm.Dispose();
        }

        private void rebootServerToolStripMenuItem_Click(object sender, EventArgs e)
        {
            commandHandler.execute("rebt");
            commandHandler.stopStream();
            connectionForm.Dispose();
        }

        private void infoToolStripMenuItem_Click(object sender, EventArgs e)
        {
            InfoForm infoform = new InfoForm();
            infoform.Show();
        }

        private void exitServerToolStripMenuItem_Click(object sender, EventArgs e)
        {
            commandHandler.execute("exit");
            commandHandler.stopStream();
            connectionForm.Dispose();
        }

        private void exitVisionEngineToolStripMenuItem_Click(object sender, EventArgs e)
        {
            commandHandler.disconnect();
            commandHandler.stopStream();
            connectionForm.Dispose();
            this.Dispose();
        }

        private void executeButton_Click(object sender, EventArgs e)
        {
            executeButton.Enabled = false;
            OutputTextbox.Text = commandHandler.execute(InputTextbox.Text);
            InputTextbox.Text = "";
            executeButton.Enabled = true;
        }

        private void enableCustomCommandsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Height = 502;
        }

        private void saveInputPictureToolStripMenuItem_Click(object sender, EventArgs e)
        {
            lock (pictureBoxInput.Image)
            {
                pictureBoxInput.Image.Save("Input" + ImageCount + ".jpg", System.Drawing.Imaging.ImageFormat.Jpeg);
                ImageCount++;
            }
        }

        private void saveOutputPictureToolStripMenuItem_Click(object sender, EventArgs e)
        {
            lock (pictureBoxOutput.Image)
            {
                pictureBoxOutput.Image.Save("Output" + ImageCount + ".jpg", System.Drawing.Imaging.ImageFormat.Jpeg);
                ImageCount++;
            }
        }

        private void VisionEngineForm_Load(object sender, EventArgs e)
        {

        }

        private void balloon1_Click(object sender, EventArgs e)
        {

        }

    }
}
