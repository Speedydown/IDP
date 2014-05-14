using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Windows.Networking;
using Windows.Networking.Sockets;
using Windows.Storage.Streams;

namespace App_Spin.Network
{
    class NetworkHandler
    {
        private static StreamSocket socket;
        private static HostName hostname;
        private static DataReader reader;
        private static DataWriter writer;
        public static NetworkBuffer InputBuffer;

        public static async Task Connect(string Hostname)
        {
            socket = new StreamSocket();
            hostname = new HostName(Hostname);
            InputBuffer = new NetworkBuffer();

            try
            { 
                await socket.ConnectAsync(hostname, "1337");
            }
            catch (Exception e)
            {
                switch (SocketError.GetStatus(e.HResult))
                {
                    case SocketErrorStatus.HostNotFound:
                        break;
                    case SocketErrorStatus.UnreachableHost:
                        break;
                    default:
                        break;
                }
            }

            // add after calling ConnectAsync on the StreamSocket Object
            reader = new DataReader(socket.InputStream);
            writer = new DataWriter(socket.OutputStream);
            InputBuffer.Append("Connected to: " + hostname + "!");
        }

        public static async Task Recv()
        {
            // container for the received Data
            string receivedData;
            reader.InputStreamOptions = InputStreamOptions.Partial;
            var count = await reader.LoadAsync(4096);

            // read the data as a string and store it in our container
            if (count > 0)
            {
                receivedData = reader.ReadString(count);
                InputBuffer.Append(receivedData);
            }
        }

        public static async Task Send(string Data)
        {
            // write a string to the OutputStream
            if (Data.Length > 0)
            {
                writer.WriteString(Data);
                // commit and send the data in the OutputStream
                await writer.StoreAsync();
            }
        }


    }
}
