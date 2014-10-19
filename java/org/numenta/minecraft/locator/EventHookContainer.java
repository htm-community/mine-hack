package org.numenta.minecraft.locator;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

import cpw.mods.fml.common.eventhandler.SubscribeEvent;
import net.minecraft.client.Minecraft;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.world.World;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.event.entity.player.PlayerEvent.StartTracking;

public class EventHookContainer {
	
	private Socket socket;
	private PrintWriter out;
	private BufferedReader in;
	
	
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
	public void playerDoesAnything(StartTracking event) {
		EntityPlayer player = (EntityPlayer) event.entity;
		String location = player.posX + "," + player.posY + "," + player.posZ;
//		World world = Minecraft.getMinecraft().theWorld;
//    	if (world != null) {
//        	world.spawnParticle("instantSpell", player.posX, player.posY, player.posZ, 0.0, 0.0, 0.0);    		
//    	}
    	try {
			out.println(location);    		
    	} catch (Exception e) {
    		e.printStackTrace();
    	}
    }

}
