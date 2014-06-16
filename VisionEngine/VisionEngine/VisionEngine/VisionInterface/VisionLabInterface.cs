using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VisionEngine.VisionInterface
{
    public abstract class VisionLabInterface
    {
        protected VisionEngineForm visionEngine; 
        protected CommandHandler commandHandler;

        public static int imgWidth = 640;
        public static int imgHeight = 480;

        protected string activeScript;

        //private abstract void setImage();

        public abstract Bitmap processImage(Bitmap bmpPicture);

        public abstract void determineMotion(int xCoordinate);



    }
}
