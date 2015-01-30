package org.numenta.minecraft.locator;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Date;

import cpw.mods.fml.common.eventhandler.SubscribeEvent;
import net.minecraft.client.Minecraft;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.world.World;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.event.entity.player.PlayerEvent.StartTracking;
import net.minecraftforge.event.world.WorldEvent;

public class EventHookContainer {
	
	private Socket socket;
	private PrintWriter out;
	private BufferedReader in;
	private String lastLocation = "";
	
	public EventHookContainer() {
		
		try {
			socket = new Socket("localhost", 50007);
			out = new PrintWriter(socket.getOutputStream(), true);
			in =  new BufferedReader(new InputStreamReader(socket.getInputStream()));
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	@SubscribeEvent
	public void worldClose(WorldEvent.Unload event) {
		// Close socket on game exit.
		out.close();
	}
	
	@SubscribeEvent
	public void playerDoesAnything(StartTracking event) {
		EntityPlayer player = (EntityPlayer) event.entity;
		String location = player.posX + "," + player.posY + "," + player.posZ;
		long gameTime = new Date().getTime();
		String message = location + " " + gameTime;
		if (! this.lastLocation.equals(location)) {
	    	try {
	    		System.out.println("Writing to socket: " + message);
				out.println(message);    		
	    	} catch (Exception e) {
	    		e.printStackTrace();
	    	}			
		}
		this.lastLocation = location;
    }

}
