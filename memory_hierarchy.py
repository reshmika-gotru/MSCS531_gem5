# Create a simple memory hierarchy with L1 and L2 caches
import m5
from m5.objects import System, SrcClockDomain, VoltageDomain, X86TimingSimpleCPU, SystemXBar, Root, MemCtrl, DDR3_1600_8x8
from caches import L1ICache, L1DCache, L2Cache
from m5.params import Clock

class MySystem(System):
    def _init_(self, opts):
        super(MySystem, self)._init_()

        # Set up system
        self.clk_domain = m5.objects.SrcClockDomain()
        self.clk_domain.clock =Clock('1GHz')
        self.clk_domain.voltage_domain = m5.objects.VoltageDomain()

        self.mem_mode = 'timing'
        self.mem_ranges = [m5.objects.AddrRange('512MB')]

        # Create CPU
        self.cpu = X86TimingSimpleCPU()

        # Attach L1 caches
        self.cpu.icache = L1ICache(opts)
        self.cpu.dcache = L1DCache(opts)
        self.l2cache = L2Cache(opts)

        # Create system bus
        self.membus = SystemXBar()

        # Connect L1 caches to CPU
        self.cpu.icache.connectCPU(self.cpu)
        self.cpu.dcache.connectCPU(self.cpu)

        # Connect L1 to L2 cache
        self.cpu.icache.connectBus(self.membus)
        self.cpu.dcache.connectBus(self.membus)

        # Connect L2 cache to memory bus
        self.l2cache.connectCPUSideBus(self.membus)

        # Create memory controller
        self.mem_ctrl = MemCtrl()
        self.mem_ctrl.dram = DDR3_1600_8x8()
        self.mem_ctrl.dram.range = self.mem_ranges[0]

        # Connect memory controller to system bus
        self.mem_ctrl.port = self.membus.mem_side_ports

# Create system and root object
opts = None  # Use default options
system = MySystem(opts)
root = Root(full_system=False, system=system)

# Instantiate the simulation
m5.instantiate()
print("Beginning gem5 simulation...")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")