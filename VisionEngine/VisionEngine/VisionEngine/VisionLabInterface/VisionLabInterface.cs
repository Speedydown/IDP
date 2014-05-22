using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;

namespace VisionEngine.VisionLabInterface
{
    class VisionLabInterface
    {
        public VisionLabInterface() { }

        public void processImage() { //Bitmap bmp
            Bitmap bmpPicture = (Bitmap)Image.FromFile("image22.jpg");
            JL_VisionLib_V3.CmdInt.Execute("icall findBalloonRed.jls");
            JL_VisionLib_V3.CmdInt.SetImage("img", "RGB", bmpPicture);
        }
    }
}

