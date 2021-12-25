using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace WpfApp1
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            RefreshVirtualMachines();
        }

        private void RefreshVirtualMachines()
        {
            listboxVirtualMachines.Items.Clear();
            textboxUuidBios.Text = null;
            var documentsPath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            string[] directories = System.IO.Directory.GetDirectories($"{documentsPath}\\Virtual Machines");
            foreach (var virtualMachinePath in directories)
            {
                var virtualMachineFiles = System.IO.Directory.GetFiles(virtualMachinePath);
                foreach (string virtualMachineFile in virtualMachineFiles)
                {
                    if (System.IO.Path.GetExtension(virtualMachineFile) == ".vmx")
                    {
                        listboxVirtualMachines.Items.Add(virtualMachineFile);
                    }
                }
            }
        }

        private void buttonRefresh_Click(object sender, RoutedEventArgs e)
        {
            RefreshVirtualMachines();
        }

        private void listboxVirtualMachines_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            textboxUuidBios.Text = null;
            if (listboxVirtualMachines.SelectedItem != null)
            {
                var virtualMachine = listboxVirtualMachines.SelectedItem.ToString();
                if (System.IO.File.Exists(virtualMachine))
                {
                    string[] lines = System.IO.File.ReadAllLines(virtualMachine);
                    foreach (var line in lines)
                    {
                        if (line.StartsWith("uuid.bios = \"") && line.EndsWith("\""))
                        {
                            string uuid = line.RemovePrefix("uuid.bios = \"").RemoveSuffix("\"");
                            textboxUuidBios.Text = uuid;
                        }
                    }
                }
            }
        }

        private void buttonRandomise_Click(object sender, RoutedEventArgs e)
        {
            string guid = Guid.NewGuid().ToString().Replace("-", "");
            System.Text.StringBuilder sb = new();
            for (int i = 0; i < guid.Length; i++)
            {
                if (i != 0 && i % 2 == 0)
                {
                    sb.Append(" ");
                }
                sb.Append(guid[i]);
            }
            string randomUuid = sb.ToString().Remove(23, 1).Insert(23, "-");
            textboxUuidBios.Text = randomUuid;
        }

        private void buttonSave_Click(object sender, RoutedEventArgs e)
        {
            if (listboxVirtualMachines.SelectedItem != null)
            {
                string virtualMachine = listboxVirtualMachines.SelectedItem.ToString();
                if (System.IO.File.Exists(virtualMachine))
                {
                    string[] lines = System.IO.File.ReadAllLines(virtualMachine);
                    string newLines = "";
                    foreach (var line in lines)
                    {
                        if (!line.StartsWith("uuid.bios = \"") && !line.StartsWith("uuid.action = \""))
                        {
                            if (newLines != "")
                            {
                                newLines = $"{newLines}\r\n{line}";
                            }
                            else
                            {
                                newLines = $"{line}";
                            }

                        }
                    }
                    if (newLines != "")
                    {
                        newLines = $"{newLines}\r\nuuid.bios = \"{textboxUuidBios.Text}\"\r\nuuid.action = \"keep\"\r\n";
                    }
                    else
                    {
                        newLines = $"uuid.bios = \"{textboxUuidBios.Text}\"\r\nuuid.action = \"keep\"\r\n";
                    }
                    System.IO.File.WriteAllText(virtualMachine, newLines);
                }
            }
        }
    }

    public static class Extensions
    {
        public static string RemovePrefix(this string str, string strStartValue)
        {
            if (str.StartsWith(strStartValue))
            {
                str = str.Remove(0, strStartValue.Length);
            }
            return str;
        }

        public static string RemoveSuffix(this string str, string strEndValue)
        {
            if (str.EndsWith(strEndValue))
            {
                str = str.Remove(str.Length - strEndValue.Length, strEndValue.Length);
            }
            return str;
        }
    }
}
