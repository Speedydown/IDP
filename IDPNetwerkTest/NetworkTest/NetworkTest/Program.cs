﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NetworkTest
{
    class Program
    {
        static void Main(string[] args)
        {
            AsynchronousClient.StartClient();
            Console.ReadLine();
            AsynchronousClient.quit = true;

        }
    }
}
