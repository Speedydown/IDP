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

    }
}
