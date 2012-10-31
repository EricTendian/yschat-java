import java.io.*;
import java.math.BigInteger;
import java.net.*;
import java.text.SimpleDateFormat;
import java.util.Date;

public class YSChat {
    private String ip;
    private String ysc_mode;
    private String ysc_char;
    private String port;
    public String version;
    private String username;
    public String players[][];
    public String map;
    private Socket socket;
    public InputStream in;
    private OutputStream out;
    public boolean connected;
    private Thread keepAlive;
    private Thread listener;

    public YSChat() {}
    
    public YSChat(String ip, String port, String version, String username) {
        this.ip=ip;
        this.port=port;
        this.version=version;
        this.username=username;
    }

    @Override
    public String toString() {
        return "YSChat{" + "ip:port=" + ip + ":" + port + " version=" + version + " username=" + username + '}';
    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public String getPort() {
        return port;
    }

    public void setPort(String port) {
        this.port = port;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setVersion(String version) {
        this.version = version;
    }

    public void connect() throws IOException {if (!connected) {
        socket = new Socket(ip, Integer.parseInt(port));
        in = socket.getInputStream();
        out = socket.getOutputStream();
        String packet;
        if (StringToHex(username).length()>30) {
            packet = "1800000001000000"+StringToHex(username).substring(0, 30);
            packet+="00"+version;
        } else {
            packet = "1800000001000000"+StringToHex(username);
            for (int i=0; i<15-username.length(); i++) {packet+="00";}
            packet+="00"+version;
        }
        byte[] b = new BigInteger(packet, 16).toByteArray();
        out.write(b);
        connected=true;
        servInfo();
        SendMess30s SendMess30s = new SendMess30s(keepAlive);
        keepAlive = new Thread(SendMess30s);
        keepAlive.start();
        OutputListener OutputListener = new OutputListener(listener);
        listener = new Thread(OutputListener);
        listener.start();

        String connectMess = "***You are connected***\n";

        if (ip.equals("127.0.0.1")) {ysc_mode = "SERVER"; ysc_char = "~";} else {ysc_mode = "CLIENT, use the ip 127.0.0.1 to be in server mode"; ysc_char = "*";}
            try {
                YSC_gui.messOut.setText(YSC_gui.messOut.getText() + connectMess + ">>>" + ysc_mode + "\n");
            } catch (NullPointerException ex) {
            try {
                YSC_applet.messOut.setText(YSC_gui.messOut.getText() + connectMess + ">>>" + ysc_mode + "\n");
            } catch (NullPointerException ex2) {System.out.println(connectMess + ">>>" + ysc_mode);}}}
    }

    public void disconnect() throws IOException {
        if (connected) {socket.close(); connected=false; keepAlive.stop(); listener.stop();
            String disconnMess = "***Connection stopped*** (conversation saved in logfile"+new SimpleDateFormat("yyyyMMdd").format(new Date())+".htm)\n";
            try {
                YSC_gui.messOut.setText(YSC_gui.messOut.getText() + disconnMess);
            } catch (NullPointerException ex) {
            try {
                YSC_applet.messOut.setText(YSC_applet.messOut.getText() + disconnMess);
            } catch (NullPointerException ex2) {System.out.println(disconnMess);}}}
    }

    public void sendMess(String mess) throws IOException {
        if (connected) {
        String packet = "6C000000200000000000000000000000"+StringToHex("("+username+ysc_char+")"+mess);
        if (packet.length()<224) {
            int p = 0;
            for (int i=packet.length(); i<224; i++) {packet+="0";}
        } else {
            packet=packet.substring(0,224);
        }
        byte[] b = new BigInteger(packet, 16).toByteArray();
        out.write(b);}
    }

    public void sendMess(String mess, boolean custom) throws IOException {
        if (connected) {
        String packet = null;
        if (custom) packet = "6C000000200000000000000000000000"+StringToHex(mess);
        if (packet.length()<224) {
            int p = 0;
            for (int i=packet.length(); i<224; i++) {packet+="0";}
        } else {
            packet=packet.substring(0,224);
        }
        byte[] b = new BigInteger(packet, 16).toByteArray();
        out.write(b);}
    }

    public String[][] getPlayers() throws IOException {
        return players;
    }

    public void listPlayers() throws IOException {out.write(new BigInteger("0400000025000000", 16).toByteArray());}

    public void servInfo() throws IOException {
        byte[] b = new byte[1024];
        in.read(b);
        String result = byteToString(b);
        if (result.indexOf("/x08/x00/x00/x00/x1d/x00/x00/x00")!=-1) {
            version = result.substring(8*4, 12*4).replaceAll("/x", "");
            version = version.substring(6)+version.substring(4,6)+version.substring(2,4)+version.substring(0,2);
            version = Integer.toString(Integer.parseInt(version, 16));

            map = result.substring(result.indexOf("/x40/x00/x00/x00/x04/x00/x00/x00")+(8*4));
            map = map.substring(0, map.indexOf("/x00"));
            map = HexToString(map);
        }
    }

    private String StringToHex(String str) {
        char[] chars = str.toCharArray();
        StringBuffer hex = new StringBuffer();
        for (int i = 0; i < chars.length; i++) {
            hex.append(Integer.toHexString((int) chars[i]));
        }
        return hex.toString();
    }

    private String HexToString(String str) {
        str=str.replaceAll("/", "").replaceAll("x", "");
        byte[] b = new BigInteger(str, 16).toByteArray();
        return new String(b);
    }

    private String byteToString(byte[] b) {
        String result = "";
        for (int i = 0; i < b.length; i++) {
            result += "/x"+Integer.toString((b[i] & 0xff) + 0x100, 16).substring(1);
        }
        return result;
    }

    public String format(String mess, String type) {
        if (type!=null) {
            mess = "<span class=\""+type+"\">"+mess+"</span>";
        } else {
            if ((mess.indexOf("has left the airplane")!=-1 || mess.indexOf("took off (")!=-1) && mess.substring(0, 15).indexOf('*')==-1) {
                mess = "<span class=\"joinleave\">"+mess+"</span>";
            } else if ((mess.indexOf("INTERCEPT MISSION/ENDURANCE MODE/CLOSE AIR SUPPORT MISSION is terminated.")!=-1 && mess.indexOf('(')!=-1) ||
                        mess.indexOf("**** ENDURANCE MODE START")!=-1 || mess.indexOf("**** END ENDURANCE MODE ****")!=-1 ||
                        mess.indexOf("**** INTERCEPT MISSION START ****")!=-1 || mess.indexOf("**** END INTERCEPT MISSION ****")!=-1 ||
                        mess.indexOf("**** CLOSE AIR SUPPORT MISSION START ****")!=-1 || mess.indexOf("**** END CLOSE AIR SUPPORT MISSION ****")!=-1) {
                mess = "<span class=\"mission\">"+mess+"</span>";
            } else if (mess.indexOf("**** Server will be reset in ")!=-1) {
                mess = "<span class=\"willreset_in\">"+mess+"</span>";
            } else if (mess.indexOf("**** Resetting Server ****")!=-1 && mess.indexOf('(')==-1) {
                mess = "<span class=\"reset_server\">"+mess+"</span>";
            } else if ((mess.indexOf("** This Server Disables Chat. **")!=-1 || mess.indexOf("** Cannot Send the Message. **")!=-1) && mess.indexOf('(')==-1) {
                mess = "<span class=\"disable_chat\">"+mess+"</span>";
            } else if (mess.substring(0, 1).equals("(") && mess.indexOf(")")!=-1) {
                int paren = mess.indexOf(")");
                mess = "<span class=\"pilotnicknam\">"+mess.substring(0,paren+1)+"</span>"+"<span class=\"default_mess\">"+mess.substring(paren+1)+"</span>";
            }
            mess = "<span class=\"time\">"+new SimpleDateFormat("[HH:mm:ss]").format(new Date())+"</span>"+mess;
        }
        return mess;
    }



    class SendMess30s implements Runnable {
        Thread SendMess30s;
        public SendMess30s(Thread t) {
            SendMess30s = t;
        }
        public void run() {
            while (connected) {
                try {
                    //byte[] b = new BigInteger("0400000025000000", 16).toByteArray();
                    //out.write(b);
                    listPlayers();
                    Thread.sleep(30000);
                } catch (InterruptedException ex) {
                    SendMess30s.stop();
                } catch (IOException ex) {
                    System.out.println(ex);
                    connected = false;
                    SendMess30s.stop();
                }
            }
        }
        public void stop() {
            SendMess30s.stop();
        }
    }

    class OutputListener implements Runnable {
        Thread OutputListener;
        String listplayer = "/x00/x00/x25/x00/x00/x00";
        public OutputListener (Thread t) {OutputListener = t;}
        public void run() {
            while (connected) {
                try {
                    byte[] b = new byte[2048];
                    in.read(b);
                    String mess = byteToString(b);
                    int is_mess = mess.indexOf("/x00/x00/x00/x20/x00/x00/x00/x00/x00/x00/x00/x00/x00/x00/x00");
                    if (mess.indexOf("/x00/x00/x2c/x00/x00/x00/x01")!=-1) {
                        byte[] reply = new BigInteger(mess.substring(mess.indexOf("/x00/x00/x2c/x00/x00/x00/x01")-2*4,mess.length()).replaceAll("/x",""), 16).toByteArray();
                        out.write(reply);
                    } 
                    if (mess.indexOf(listplayer) != -1) {
                        int player = 0;
                        for (int i=0; i<mess.length()-6*4; i++) {
                            if (mess.substring(i, i+6*4).equals(listplayer)) player+=1;
                        }
                        players = new String[player][3];
                        player = 0;
                        while (player<players.length) {
                            String mess1;
                            String status;
                            String iff;
                            String id;
                            String user;
                            int pos = mess.indexOf(listplayer) + 6*4;
                            mess1 = mess.substring(pos);
                            user = HexToString(mess1.substring(12*4).substring(0, mess1.substring(12*4).indexOf("/x00"))).trim();
                            if (mess1.indexOf(listplayer)!=-1) {
                                pos = mess1.indexOf(listplayer);
                                user = HexToString(mess1.substring(12*4, pos));
                                mess1 = mess1.substring(0, pos-6*4);
                            }
                            
                            status = mess1.substring(3,4);
                            iff = Integer.toString(Integer.parseInt(mess1.substring(2*4,3*4).replaceAll("/", "").replaceAll("x", ""), 16)+1);
                            id = mess1.substring(4*4,7*4).replaceAll("/x", "");
                            id = Integer.toString(Integer.parseInt(id.substring(4,6)+id.substring(2,4)+id.substring(0,2), 16));
                            status = status.trim();
                            iff = iff.trim();
                            id = id.trim();
                            user = user.trim();
                            
                            if (status.equals("1"))      {players[player][0]=id;    players[player][1]=user; players[player][2]=iff;}
                            else if (status.equals("2")) {players[player][0]="N/A"; players[player][1]=user; players[player][2]="SERVER";}
                            else if (status.equals("3")) {players[player][0]=id;    players[player][1]=user; players[player][2]=iff+" (SERVER)";}
                            else                         {players[player][0]="N/A"; players[player][1]=user; players[player][2]="N/A";}
                            
                            mess = mess.substring(mess.indexOf(mess1)+mess1.length());
                            player+=1;
                        }
                        try {
                            while (YSC_gui.model.getRowCount() > 0) {
                                YSC_gui.model.removeRow(0);
                            }
                            for (int i = 0; i < players.length; i++) {
                                YSC_gui.model.addRow(players[i]);
                            }
                            YSC_gui.playerList.setModel(YSC_gui.model);
                        } catch (NullPointerException ex) {}

                        try {
                            while (YSC_applet.model.getRowCount() > 0) {
                                YSC_applet.model.removeRow(0);
                            }
                            for (int i = 0; i < players.length; i++) {
                                YSC_applet.model.addRow(players[i]);
                            }
                            YSC_applet.playerList.setModel(YSC_applet.model);
                        } catch (NullPointerException ex) {}
                    } is_mess = mess.indexOf("/x00/x00/x00/x20/x00/x00/x00/x00/x00/x00/x00/x00/x00/x00/x00"); while (is_mess != -1) {
                        String mess3 = "";
                        if (is_mess != -1) {
                            String mess2 = mess.substring(is_mess + 15 * 4);
                            int pos = mess2.indexOf("/x00");
                            mess2 = mess2.substring(0, pos);
                            mess = mess.substring(is_mess + 15 * 4 + pos);
                            mess3 = mess2.replaceAll("/x00", "");
                            is_mess = mess.indexOf("/x00/x00/x00/x20/x00/x00/x00/x00/x00/x00/x00/x00/x00/x00/x00");
                        }
                        mess3=HexToString(mess3).replaceAll("(-!-)", " ");
                        if (mess3.indexOf("/listusers")!=-1 && ip.equals("127.0.0.1")) {
                            listPlayers();
                            String playerlist = "";
                            for (int i=0; i<players[0].length-1; i++) {
                                playerlist+=", "+players[i][1];
                            }
                            sendMess(playerlist.substring(2), true);
                        } try {if (mess3.substring(0, 10).indexOf("nameless")!=-1)  sendMess("CHANGE YOUR USERNAME NAMELESS!");} catch (Exception ex) {}
                          if (mess3.toLowerCase().indexOf("anyone there")!=-1 || mess3.toLowerCase().indexOf("anyone here")!=-1) sendMess("/listusers");
                        
                        try {
                            YSC_gui.log_out.append(format(mess3, null)+"<br/>");
                            YSC_gui.refresh();
                        } catch (NullPointerException ex) {
                        try {
                            YSC_applet.messOut.setText(mess3);
                        } catch (NullPointerException ex2) {System.out.println(mess3);}}
                        is_mess = mess.indexOf("/x00/x00/x00/x20/x00/x00/x00/x00/x00/x00/x00/x00/x00/x00/x00");
                    }
                } catch (IOException ex) {
                    System.out.println(ex);
                    connected=false;
                }
            }
            System.out.println("connection lost to server "+ip);
        }
    }
}