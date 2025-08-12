import java.util.*;
import java.util.concurrent.*;

/**
 * JDK 8 内存测试应用
 * 用于演示 Arthas 4.x 的内存分析功能
 */
public class MemoryTestApp {
    private static final List<byte[]> memoryList = new ArrayList<>();
    private static final Map<String, Object> dataMap = new ConcurrentHashMap<>();
    private static volatile boolean running = true;
    
    public static void main(String[] args) {
        System.out.println("=== JDK 8 Memory Test Application Started ===");
        System.out.println("Java Version: " + System.getProperty("java.version"));
        System.out.println("JVM Name: " + System.getProperty("java.vm.name"));
        System.out.println("Max Memory: " + (Runtime.getRuntime().maxMemory() / 1024 / 1024) + " MB");
        System.out.println("Process ID: " + getProcessId());
        
        // 注册关闭钩子
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("=== Shutdown hook triggered ===");
            running = false;
        }));
        
        // 启动内存分配线程
        Thread memoryThread = new Thread(MemoryTestApp::allocateMemory, "MemoryAllocator");
        Thread dataThread = new Thread(MemoryTestApp::generateData, "DataGenerator");
        
        memoryThread.start();
        dataThread.start();
        
        // 主线程保持运行
        try {
            while (running) {
                Thread.sleep(5000);
                printMemoryStats();
            }
        } catch (InterruptedException e) {
            System.out.println("Main thread interrupted");
        }
        
        System.out.println("=== Application shutting down ===");
    }
    
    /**
     * 分配内存块
     */
    private static void allocateMemory() {
        int blockSize = 1024 * 1024; // 1MB blocks
        int maxBlocks = 100;
        
        try {
            while (running && memoryList.size() < maxBlocks) {
                byte[] block = new byte[blockSize];
                // 填充一些数据
                Arrays.fill(block, (byte) (memoryList.size() % 256));
                memoryList.add(block);
                
                System.out.println("Allocated memory block #" + memoryList.size() + 
                                 " (Size: " + blockSize + " bytes)");
                
                Thread.sleep(2000);
            }
            
            System.out.println("Memory allocation completed. Total blocks: " + memoryList.size());
            
            // 保持内存占用
            while (running) {
                Thread.sleep(10000);
            }
        } catch (InterruptedException e) {
            System.out.println("Memory allocation thread interrupted");
        }
    }
    
    /**
     * 生成测试数据
     */
    private static void generateData() {
        Random random = new Random();
        
        try {
            while (running) {
                // 生成字符串数据
                for (int i = 0; i < 1000; i++) {
                    String key = "key_" + i + "_" + System.currentTimeMillis();
                    String value = "value_" + random.nextInt(10000);
                    dataMap.put(key, value);
                }
                
                // 定期清理旧数据
                if (dataMap.size() > 5000) {
                    Iterator<String> iterator = dataMap.keySet().iterator();
                    int removeCount = 0;
                    while (iterator.hasNext() && removeCount < 2000) {
                        iterator.next();
                        iterator.remove();
                        removeCount++;
                    }
                    System.out.println("Cleaned up " + removeCount + " old data entries");
                }
                
                Thread.sleep(3000);
            }
        } catch (InterruptedException e) {
            System.out.println("Data generation thread interrupted");
        }
    }
    
    /**
     * 打印内存统计信息
     */
    private static void printMemoryStats() {
        Runtime runtime = Runtime.getRuntime();
        long totalMemory = runtime.totalMemory();
        long freeMemory = runtime.freeMemory();
        long usedMemory = totalMemory - freeMemory;
        long maxMemory = runtime.maxMemory();
        
        System.out.println("=== Memory Statistics ===");
        System.out.println("Used Memory: " + (usedMemory / 1024 / 1024) + " MB");
        System.out.println("Free Memory: " + (freeMemory / 1024 / 1024) + " MB");
        System.out.println("Total Memory: " + (totalMemory / 1024 / 1024) + " MB");
        System.out.println("Max Memory: " + (maxMemory / 1024 / 1024) + " MB");
        System.out.println("Memory Blocks: " + memoryList.size());
        System.out.println("Data Map Size: " + dataMap.size());
        System.out.println("========================");
    }
    
    /**
     * 获取进程ID (JDK 8 兼容方式)
     */
    private static String getProcessId() {
        try {
            String jvmName = java.lang.management.ManagementFactory.getRuntimeMXBean().getName();
            return jvmName.split("@")[0];
        } catch (Exception e) {
            return "unknown";
        }
    }
}