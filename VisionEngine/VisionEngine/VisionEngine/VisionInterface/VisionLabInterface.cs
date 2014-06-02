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
        private VisionEngineForm visionEngine;

        public VisionLabInterface(VisionEngineForm ve)
        {
            this.visionEngine = ve;
        }

        private void setImage(int indexColor, int indexRank)
        {
            switch (indexColor)
            {
                case 0:
                    visionEngine.Invoke(visionEngine.UpdateImageBalloonDelegate, new Object[] { "RED", indexRank });
                    break;
                case 1:
                    visionEngine.Invoke(visionEngine.UpdateImageBalloonDelegate, new Object[] { "GREEN", indexRank });
                    break;
                case 2:
                    visionEngine.Invoke(visionEngine.UpdateImageBalloonDelegate, new Object[] { "BLUE", indexRank });
                    break;
            }
        }



        public Bitmap processImage(Bitmap bmpPicture)
        {
            // Bitmap bmpPicture = (Bitmap)Image.FromFile("image.jpg");
            JL_VisionLib_V3.CmdInt.Execute("addScript findballoon analyseCard.jls");
            JL_VisionLib_V3.CmdInt.Execute("$iks = 12");
            JL_VisionLib_V3.CmdInt.SetImage("img", "RGB888Image", bmpPicture);

            String result = JL_VisionLib_V3.CmdInt.Execute("icall findballoon");

            
            if (result != "-1")
            {
                List<string> values = result.Split(' ').ToList();
                bool correctInput = Convert.ToBoolean(values[values.Count() - 1]);
                values.RemoveAt(values.Count() - 1);

                List<int> yValues = new List<int>();
                
                foreach (string s in values)
                {
                    //Console.WriteLine(s);
                    yValues.Add(Convert.ToInt16(s));
                }
                
                if (correctInput) {
                    List<int> yValuesCopy = new List<int>(yValues);
                    yValuesCopy.Sort();
                    Console.WriteLine("YYY" + yValues.First(item => item == yValuesCopy[2]));
                    this.setImage(yValues.FindIndex(item => item == yValuesCopy[2]),3);
                    this.setImage(yValues.FindIndex(item => item == yValuesCopy[1]), 2);
                    this.setImage(yValues.FindIndex(item => item == yValuesCopy[0]), 1);

                    //int high = yValuesCopy[2];
                    //int mid = yValuesCopy[1];
                    //int low = yValuesCopy[0];
                 
                }
            }
           


            return JL_VisionLib_V3.CmdInt.GetImage("img");
        }
    }
}

