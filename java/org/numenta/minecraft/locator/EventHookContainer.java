package org.numenta.minecraft.locator;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

import cpw.mods.fml.common.eventhandler.SubscribeEvent;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.event.entity.player.PlayerEvent.StartTracking;

public class EventHookContainer {
	
	private Socket socket;
	private PrintWriter out;
	
	public EventHookContainer() {
		try {
			socket = new Socket("localhost", 50007);
			out = new PrintWriter(socket.getOutputStream(), true);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	@SubscribeEvent
	public void playerDoesAnything(StartTracking event) {
		EntityPlayer player = (EntityPlayer) event.entity;
    	String location = player.posX + "," + player.posY + "," + player.posZ;
	    System.out.println(location);
    	try {
			out.println(location);    		
    	} catch (Exception e) {
    		e.printStackTrace();
    	}
    }

}
