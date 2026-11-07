# Normalized ellipse spans: one table per vertical radius. Horizontal radius
# scales the half-width with one multiply; only visible scanlines are visited.
import math
ellipse=[]
for h in range(1,513):
 ellipse.append(asset('ellipse36c_'+str(h),struct.pack('>'+str(h+1)+'H',*[round(math.sqrt(max(0,1-(y/(h+0.5))**2))*256) for y in range(h+1)])))
ep=asset('ellipse_ptrs36c',struct.pack('>512I',*ellipse))
c.label('ellipse_draw36c');c.emit('302800060c400200');c.branch('6200','ellipse_native36c')
c.emit('4a40');c.branch('6600','ellipse_height36c');c.emit('7001')
c.label('ellipse_height36c');c.emit('3c003e2800049e403a280004da40')
c.emit('4a47');c.branch('6a00','ellipse_top36c');c.emit('7e00')
c.label('ellipse_top36c');c.emit('0c45007f');c.branch('6f00','ellipse_bottom36c');c.emit('7a7f')
c.label('ellipse_bottom36c');c.emit('be45');c.branch('6e00','ellipse_done36c')
c.emit('5340e548');c.abs('45f9',ep);c.emit('24720000')
c.label('ellipse_row36c');c.emit('300790680004');c.branch('6a00','ellipse_abs36c');c.emit('4440')
c.label('ellipse_abs36c');c.emit('d04034320000c4e80008e08a302800029042d46800023207');c.call(0xe074)
c.emit('5247be45');c.branch('6f00','ellipse_row36c')
c.label('ellipse_done36c');c.emit('4e75')
c.label('ellipse_native36c');c.emit(src[0xd4a0:0xd4a6].hex());c.jump(0xd4a6);patch(0xd4a0,'ellipse_draw36c')
