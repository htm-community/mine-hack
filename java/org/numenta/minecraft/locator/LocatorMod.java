package org.numenta.minecraft.locator;

import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.entity.player.PlayerEvent;
import cpw.mods.fml.common.Mod;
import cpw.mods.fml.common.Mod.EventHandler; // used in 1.6.2
//import cpw.mods.fml.common.Mod.PreInit;    // used in 1.5.2
//import cpw.mods.fml.common.Mod.Init;       // used in 1.5.2
//import cpw.mods.fml.common.Mod.PostInit;   // used in 1.5.2
import cpw.mods.fml.common.Mod.Instance;
import cpw.mods.fml.common.SidedProxy;
import cpw.mods.fml.common.event.FMLInitializationEvent;
import cpw.mods.fml.common.event.FMLPostInitializationEvent;
import cpw.mods.fml.common.event.FMLPreInitializationEvent;
//import cpw.mods.fml.common.network.NetworkMod; // not used in 1.7

@Mod(modid="LocatorModID", name="LocatorMod", version="0.0.0")
//@NetworkMod(clientSideRequired=true) // not used in 1.7
public class LocatorMod {

        // The instance of your mod that Forge uses.
        @Instance(value = "LocatorModID")
        public static LocatorMod instance;
        
        // Says where the client and server 'proxy' code is loaded.
        @SidedProxy(clientSide="org.numenta.minecraft.locator.client.ClientProxy", serverSide="org.numenta.minecraft.locator.CommonProxy")
        public static CommonProxy proxy;
        
        @EventHandler // used in 1.6.2
        //@PreInit    // used in 1.5.2
        public void preInit(FMLPreInitializationEvent event) {
                // Stub Method
        	System.out.println("pre init");
        }
        
        @EventHandler // used in 1.6.2
        //@Init       // used in 1.5.2
        public void load(FMLInitializationEvent event) {
                proxy.registerRenderers();
            	System.out.println("load");
            	MinecraftForge.EVENT_BUS.register(new EventHookContainer());
        }
        
        @EventHandler // used in 1.6.2
        //@PostInit   // used in 1.5.2
        public void postInit(FMLPostInitializationEvent event) {
        	System.out.println("post init");
        }
        
}