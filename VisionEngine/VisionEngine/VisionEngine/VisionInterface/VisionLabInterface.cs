using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VisionEngine.VisionInterface
{
    abstract class VisionLabInterface
    {
        protected VisionEngineForm visionEngine; 
        protected CommandHandler commandHandler;

        protected string activeScript;

        //private abstract void setImage();

        public abstract Bitmap processImage(Bitmap bmpPicture);

        public abstract void determineMotion();



    }
}
