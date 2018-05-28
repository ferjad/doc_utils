using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Text.RegularExpressions;
namespace Parser
{
    class Program
    {
      //port number and IP address
      const int PORT_NO = 9400;
      const string SERVER_IP = "0.0.0.0";
      public static string dateparser(string text){
        string output = "";
        //match regex to get dates
        MatchCollection matches = Regex.Matches(text, @"\d+[./-]\d+[./-]\d+|\w{3,9}?\s\d{1,2}?\s?,\s\d{4}?|\d{1,2}?\s\w{3,9}?\s\d{4}?");
        foreach (Match match in matches)
        {
          foreach (Capture capture in match.Captures)
          {
            output = output + capture.Value + "\n";
          }
        }
        return output;
      }

      static void Main(string[] args)
      {
        //listen on the port and ip
        IPAddress localAdd = IPAddress.Parse(SERVER_IP);
        TcpListener listener = new TcpListener(localAdd, PORT_NO);
        Console.WriteLine("Listening...");
        listener.Start();

        //run listener in infinite loop
        while (true)
        {
            //client connected
            TcpClient client = listener.AcceptTcpClient();

            //network stream to get incoming data
            NetworkStream nwStream = client.GetStream();
            byte[] buffer = new byte[client.ReceiveBufferSize];

            //-read data
            int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize);

            //data to string
            string dataReceived = Encoding.ASCII.GetString(buffer, 0, bytesRead);


            //parse the input to get dates
            string response = dateparser(dataReceived);

            //comvert dateparser output to bytes
            byte[] responseBuffer = Encoding.ASCII.GetBytes(response);

            //send output to client
            nwStream.Write(responseBuffer, 0, responseBuffer.Length);
            //close client connection
            client.Close();
        }

        listener.Stop();
      }
    }
}
