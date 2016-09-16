def create_segment(startea,endea, segment_name=None, base_paragraph=0x0, use32=1, align=0, comb=0, flags=0):
  if AddSegEx( startea, endea, base_paragraph, use32, align, comb, flags) == 0:
    return False
  if segment_name is not None:
    if RenameSeg( startea, segment_name) == 0:
      return False
  return True

def load_file(filename, ea, file_offset=0,  size=0, end_ea=0):
    if size == 0 and end_ea == 0:
        raise "invalid call to load_file, size and end_ea both 0"
    else:
        if size == 0:
            size = end_ea-ea
    if end_ea == 0:
        end_ea = ea + size

    path = os.path.abspath(filename)
    li = idaapi.open_linput(path, False)
    if not li:
        raise 'Unable to create loader_input_t : %s' % path
    res = idaapi.file2base(li, file_offset, ea, end_ea, True)
    idaapi.close_linput(li)
    return res

def make_dwords(ea,end_ea):
    for ea in xrange(ea,end_ea,4):
        MakeData(ea,FF_DWRD,4,0)

#  assert load_file(AskFile(0,"dc24-userapp.bin",""), ea=0x180000, size=0x200000)

assert load_file(AskFile(0,"dc24-rom.bin",""), ea=0, size=0x1fff)

assert load_file(AskFile(0,"dc24-sram.bin",""), ea=0x280000, size=0x1fff)
#  make_dwords(0x280000,0x280fff)

#  assert load_file(AskFile(0,"dc24-dataflash.bin",""), ea=0x200000, size=0xfff)
assert load_file(AskFile(0,"dc24-otpdata.bin",""), ea=0x200000, size=0xfff)


assert create_segment(0xFEE00000, 0xFEE00FFF, "LAPIC")
assert create_segment(0xFEC00000, 0xFECFFFFF, "IOAPIC")
assert create_segment(0xB0800000, 0xB0803FFF, "SCSS")
assert create_segment(0xB0700000, 0xB0700FFF, "DMA")
assert create_segment(0xB0400000, 0xB04003FF, "SRAM_Config")
assert create_segment(0xB0100000, 0xB01003FF, "FLASH_Config")
assert create_segment(0xB0004000, 0xB00043FF, "ADC")
assert create_segment(0xB0002800, 0xB0002BFF, "I2C0")
assert create_segment(0xB0002400, 0xB00027FF, "UARTB")
assert create_segment(0xB0002000, 0xB00023FF, "UARTA")
assert create_segment(0xB0001800, 0xB0001BFF, "SPIS")
assert create_segment(0xB0001000, 0xB00013FF, "SPIM0")
assert create_segment(0xB0000C00, 0xB0000FFF, "GPIO")
assert create_segment(0xB0000800, 0xB0000BFF, "APBTimer")
assert create_segment(0xB0000400, 0xB00007FF, "RTC")
assert create_segment(0xB0000000, 0xB00003FF, "WatchdogTimer")
assert create_segment(0x00280000, 0x00281FFF, "SRAM")
assert create_segment(0x00200000, 0x00200FFF, "OTPDATA")
assert create_segment(0x00180000, 0x00187FFF, "FLASH")

#code
assert create_segment(0x00000000, 0x00001FFF, "CODE")


make_dwords(0,0x1fff)
make_dwords(0x200000,0x200fff)

#  vim: set ft=python tw=0 ts=2 sw=4 sts=2 fdm=marker fmr={{{,}}} et:
