using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VisionEngine
{
    class Balloon :IComparable<Balloon>
    {
        public int index { get; private set;}
        public Color color { get; private set; }
        public string script = "";
        public string testImage = "";

        public Balloon(int index, Color color) {
            this.index = index;
            this.color = color;
            switch (color.Name) {
                case "Red":
                    script = "findBalloonRed";
                    break;
                case "Green":
                    script = "findBalloonGreen";
                    break;
                case "Blue":
                    script = "findBalloonBlue";
                    break;                    
            }

            //Console.WriteLine(color.Name);
        }


        public void findBalloon()
        {
           
            JL_VisionLib_V3.CmdInt.Execute("addScript findballoon findBalloon" + this.color.Name +".jls");
            JL_VisionLib_V3.CmdInt.Execute("icall findballoon");
            Console.WriteLine("Searching for " + this.color.Name + " balloon");
        }

        public int CompareTo(Balloon b2)
        {
            return this.index.CompareTo(b2.index);
        }

        public override string ToString()
        {
            return String.Format("Balloon: {0} at index: {1}", this.color.ToString(), this.index.ToString());
        }
    }

}
