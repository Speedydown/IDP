using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VisionEngine.VisionInterface
{
    public class VisionLabInterface
    {
        public VisionLabInterface() { }

        public Bitmap processImage(Bitmap bmpPicture)
        {
            // Bitmap bmpPicture = (Bitmap)Image.FromFile("image.jpg");
            JL_VisionLib_V3.CmdInt.Execute("addScript findballoon findBalloonRed.jls");
            JL_VisionLib_V3.CmdInt.SetImage("img", "RGB888Image", bmpPicture);
            Console.WriteLine(JL_VisionLib_V3.CmdInt.Execute("icall findballoon"));
            return JL_VisionLib_V3.CmdInt.GetImage("r");


        }
    }
}
