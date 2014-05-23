using JL_VisionLib_V3;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using VisionEngine.Network;

namespace VisionEngine
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent(); 
            CmdInt.Init();
            NetworkBuffer buffer = new NetworkBuffer();
            NetworkInterface networkInterface = new NetworkInterface(buffer);
            networkInterface.Send("prin Test<EOF>");
            networkInterface.Recv();
            NetworkTest.Text = buffer.Get();

            
        }
    }
}
