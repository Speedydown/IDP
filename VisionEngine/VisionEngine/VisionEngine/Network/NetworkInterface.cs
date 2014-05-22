using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;


namespace VisionEngine.Network
{
    class NetworkInterface
    {
        private NetworkBuffer _Buffer;
        private TcpClient  clientSocket = new TcpClient();
        private NetworkStream serverStream;

        public NetworkInterface()
        {
            serverStream = clientSocket.GetStream();
        }

        public void Send(string Data)
        {
            byte[] outStream = System.Text.Encoding.ASCII.GetBytes(Data);
            serverStream.Write(outStream, 0, outStream.Length);
            serverStream.Flush();

        }

        public void Recv()
        {
            byte[] inStream = new byte[1024];
            
            string Data = string.Empty;
            while (Data.Contains("<EOF>"))

            serverStream.Read(inStream, 0, (int)clientSocket.ReceiveBufferSize);
            string returndata = System.Text.Encoding.ASCII.GetString(inStream);
            
        }

    }
}
