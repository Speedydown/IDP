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
        private CommandHandler commandHandler;
        private ConnectionForm connectionForm;

        public VisionEngineForm(CommandHandler commandHandler, ConnectionForm connectionForm)
        {
            InitializeComponent();
            this.commandHandler = commandHandler;
            this.connectionForm = connectionForm;
            pictureBoxInput.SizeMode = PictureBoxSizeMode.StretchImage;
            pictureBoxOutput.SizeMode = PictureBoxSizeMode.StretchImage;
            UpdateImageDelegate = new UpdateImage(updateImages);
 
        }

        private void updateImages(Bitmap Input, Bitmap Output)
        {
            this.pictureBoxInput.Image = Input;
            this.pictureBoxOutput.Image = Output;
        }

        private void StartButton_Click(object sender, EventArgs e)
        {
            commandHandler.startStream();
        }

        private void StopButton_Click(object sender, EventArgs e)
        {
            commandHandler.stopStream();
        }

        private void ShutdownButton_Click(object sender, EventArgs e)
        {
            commandHandler.execute("shtd");
            connectionForm.Dispose();
        }



    }
}
