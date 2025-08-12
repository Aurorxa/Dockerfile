import java.util.*;
import java.lang.management.*;

public class MemoryTestApp {
    private static List<byte[]> memoryList = new ArrayList<>();
    
    public static void main(String[] args) throws Exception {
        System.out.println("Memory Test Application Started on AlmaLinux 9...");
        System.out.println("PID: " + ManagementFactory.getRuntimeMXBean().getName().split("@")[0]);
        System.out.println("Java Version: " + System.getProperty("java.version"));
        System.out.println("OS: " + System.getProperty("os.name") + " " + System.getProperty("os.version"));
        
        // Initial memory status
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        System.out.println("Initial Heap Memory: " + memoryBean.getHeapMemoryUsage());
        
        int count = 0;
        while(true) {
            if(count < 50) {
                // Allocate 1MB memory
                memoryList.add(new byte[1024]);
                count++;
                System.out.println("Allocated " + count + "MB, Heap: " + memoryBean.getHeapMemoryUsage().getUsed()/1024/1024 + "MB");
            }
            Thread.sleep(3000);
        }
    }
}