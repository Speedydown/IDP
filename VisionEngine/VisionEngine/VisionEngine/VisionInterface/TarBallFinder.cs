using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VisionEngine.VisionInterface
{
    class TarBallFinder : VisionLabInterface
    {
        public TarBallFinder(VisionEngineForm ve, CommandHandler commandHandler)
        {
            this.visionEngine = ve;
            this.commandHandler = commandHandler;
            //this.activeScript = "";
        }

        public override System.Drawing.Bitmap processImage(System.Drawing.Bitmap bmpPicture)
        {
            throw new NotImplementedException();
        }

        public override void determineMotion(int xCoordinate)
        {
            throw new NotImplementedException();
        }
    }
}
