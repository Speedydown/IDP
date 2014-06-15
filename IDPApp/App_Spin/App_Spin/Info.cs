using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace App_Spin
{
    public class Info
    {
        private static string connState;
        private static bool connected;

        public void setState(string state)
        {
            connState = state;
        }

        public string getState()
        {
            return connState;
        }

        public void setConnected(bool conn)
        {
            connected = conn;
        }

        public bool getConnected()
        {
            return connected;
        }
    }
}
