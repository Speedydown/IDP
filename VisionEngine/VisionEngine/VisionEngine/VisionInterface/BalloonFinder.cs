using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VisionEngine.VisionInterface
{
    public class BalloonFinder : VisionLabInterface
    {
        Boolean cardModus;
        List<Balloon> balloonSequence = new List<Balloon>();

        public BalloonFinder(VisionEngineForm ve, CommandHandler commandHandler)
        {
            this.visionEngine = ve;
            this.commandHandler = commandHandler;
            this.activeScript = "analyseCard2.jls";
            cardModus = true;
        }

        public override void determineMotion(int xCoordinate)
        {
            int midX = VisionLabInterface.imgWidth / 2;
            //+15 -15 == equal go forward
            if (xCoordinate > (midX - 15) && xCoordinate < (midX + 15)) { //go forward
                this.commandHandler.execute("move 11");
            } 
            if (xCoordinate < midX) { //go left
                //or left forward
                this.commandHandler.execute("move 17");
            } 
            if (xCoordinate > midX) { //go right
                this.commandHandler.execute("move 13");
            } 

            throw new NotImplementedException();
        }

        private void setBalloonImage(int color, int indexRank)
        {
            //Console.WriteLine("color: " + color.ToString() + " index: " + indexRank.ToString());
            

            switch (color)
            {
                case 0:
                    visionEngine.Invoke(visionEngine.UpdateImageBalloonDelegate, new Object[] { "RED", indexRank });
                    Balloon bRed = new Balloon(indexRank, Color.Red);
                    //bRed.testImage = "C:\\Users\\Miriam\\Desktop\\foo3.jpg";
                    balloonSequence.Add(bRed);
                 
                    break;
                case 1:
                    visionEngine.Invoke(visionEngine.UpdateImageBalloonDelegate, new Object[] { "GREEN", indexRank });
                    Balloon bGreen = new Balloon(indexRank, Color.Green);
                    //bGreen.testImage = "C:\\Users\\Miriam\\Desktop\\Input100.jpg";
                    balloonSequence.Add(bGreen);
              
                    break;
                case 2:
                    visionEngine.Invoke(visionEngine.UpdateImageBalloonDelegate, new Object[] { "BLUE", indexRank });
                    Balloon bBlue = new Balloon(indexRank, Color.Blue);
                    //bBlue.testImage = "C:\\Users\\Miriam\\Desktop\\Input6.jpg";
                    balloonSequence.Add(bBlue);
                    break;
            }

          
            //Console.WriteLine("test");

        }

        public override System.Drawing.Bitmap processImage(System.Drawing.Bitmap bmpPicture)
        {

          
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
                        List<int> yValuesCopy = new List<int>(yValues); //rgb
                        yValuesCopy.Sort(); //rgb sorted by Y value
                        this.setBalloonImage(yValues.FindIndex(item => item == yValuesCopy[2]), 3);
                        this.setBalloonImage(yValues.FindIndex(item => item == yValuesCopy[1]), 2);
                        this.setBalloonImage(yValues.FindIndex(item => item == yValuesCopy[0]), 1); //find original index, 0=r 1=g 2=b

                        Console.WriteLine("Count: " + balloonSequence.Count());
                        foreach (Balloon b in balloonSequence)
                        {
       
                            Console.WriteLine("before: " + b.ToString());
                        }

                        balloonSequence.Sort();

                        foreach (Balloon b in balloonSequence)
                        {
                            //Console.WriteLine(b.ToString());
                            Console.WriteLine("after: " + b.ToString());
                        }

                        balloonSequence[0].findBalloon();
                        //CommandHandler.input = balloonSequence[0].testImage;

                        cardModus = false;
                    }
                }

            }

            else
            {

                JL_VisionLib_V3.CmdInt.SetImage("img", "RGB888Image", bmpPicture);
                List<string> values = JL_VisionLib_V3.CmdInt.Execute("icall findballoon").Split(' ').ToList();
                int result = Convert.ToInt16(values[0]);

                if (result != -1)
                {
                    Console.WriteLine("RESULT: " + values[0] + " " + values[1]);
                    determineMotion(Convert.ToInt16(values[1]));
                    //findNextBalloon();
                    //Console.WriteLine(result);
                    //this.commandHandler.execute("move 11");
                }
                else { 
                    //turn around
                }
                //else { this.commandHandler.execute("move 10"); }
            }

            return JL_VisionLib_V3.CmdInt.GetImage("img");
        }

        public void findNextBalloon() {
            if (balloonSequence.Count() > 1) {
                balloonSequence.RemoveAt(0);
                balloonSequence[0].findBalloon();
                //CommandHandler.input = balloonSequence[0].testImage;
            }
        }
    }


}
