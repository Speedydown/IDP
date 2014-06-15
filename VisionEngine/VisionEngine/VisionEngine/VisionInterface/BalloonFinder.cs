using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VisionEngine.VisionInterface
{
    class BalloonFinder : VisionLabInterface
    {
        Boolean cardModus;

        public BalloonFinder(VisionEngineForm ve, CommandHandler commandHandler)
        {
            this.visionEngine = ve;
            this.commandHandler = commandHandler;
            this.activeScript = "analyseCard2.jls";
        }

        public override void determineMotion()
        {
            throw new NotImplementedException();
        }

        private void setBalloonImage(int color, int indexRank)
        {
            List<Balloon> balloonSequence = new List<Balloon>();

            switch (color)
            {
                case 0:
                    visionEngine.Invoke(visionEngine.UpdateImageBalloonDelegate, new Object[] { "RED", indexRank });

                    if (indexRank == 1)
                    {
                        JL_VisionLib_V3.CmdInt.Execute("addScript findballoon findBalloonRed.jls");
                        Balloon bRed = new Balloon(indexRank, Color.Red);
                    }
                    break;
                case 1:
                    visionEngine.Invoke(visionEngine.UpdateImageBalloonDelegate, new Object[] { "GREEN", indexRank });
                    if (indexRank == 1)
                    {
                        JL_VisionLib_V3.CmdInt.Execute("addScript findballoon findBalloonGreen.jls");
                        Balloon bGreen = new Balloon(indexRank, Color.Green);
                    }
                    break;
                case 2:
                    visionEngine.Invoke(visionEngine.UpdateImageBalloonDelegate, new Object[] { "BLUE", indexRank });
                    if (indexRank == 1)
                    {
                        JL_VisionLib_V3.CmdInt.Execute("addScript findballoon findBalloonBlue.jls");
                        Balloon bBlue = new Balloon(indexRank, Color.Blue);
                    }
                    break;
            }

            //balloonSequence.Sort();

            foreach (Balloon b in balloonSequence)
            {
                //Console.Write(b.ToString() + b.index);
            }



        }

        public override System.Drawing.Bitmap processImage(System.Drawing.Bitmap bmpPicture)
        {

            cardModus = true;
            if (cardModus)
            {
                // Bitmap bmpPicture = (Bitmap)Image.FromFile("image.jpg");
                JL_VisionLib_V3.CmdInt.Execute("addScript findballoon analyseCard2.jls");
                //JL_VisionLib_V3.CmdInt.Execute("addScript findballoon findBalloonBlue.jls");
                JL_VisionLib_V3.CmdInt.SetImage("img", "RGB888Image", bmpPicture);

                String result = JL_VisionLib_V3.CmdInt.Execute("icall findballoon");
                //Console.WriteLine("Result: " + result);
                //return JL_VisionLib_V3.CmdInt.GetImage("img");

                if (result != "-1")
                {
                    List<string> values = result.Split(' ').ToList();
                    bool correctInput = Convert.ToBoolean(values[values.Count() - 1]);
                    values.RemoveAt(values.Count() - 1); //remove boolean value

                    List<int> yValues = new List<int>();

                    foreach (string s in values)
                    {
                        //Console.WriteLine(s);
                        yValues.Add(Convert.ToInt16(s));
                    }

                    if (correctInput)
                    {
                        List<int> yValuesCopy = new List<int>(yValues);
                        yValuesCopy.Sort();
                        this.setBalloonImage(yValues.FindIndex(item => item == yValuesCopy[2]), 3);
                        this.setBalloonImage(yValues.FindIndex(item => item == yValuesCopy[1]), 2);
                        this.setBalloonImage(yValues.FindIndex(item => item == yValuesCopy[0]), 1);
                        cardModus = false;
                    }
                }

            }

            else
            {

                JL_VisionLib_V3.CmdInt.SetImage("img", "RGB888Image", bmpPicture);

                int result = Convert.ToInt16(JL_VisionLib_V3.CmdInt.Execute("icall findballoon"));
                Console.WriteLine("RESULT: " + result);
                if (result != -1)
                {
                    Console.WriteLine(result);
                    //this.commandHandler.execute("move 11");
                }
                //else { this.commandHandler.execute("move 10"); }
            }

            return JL_VisionLib_V3.CmdInt.GetImage("img");
        }
    }
}
