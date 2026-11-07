# Native display codes increase DOWN the building:5F..G,L1..L8.
# Parking/Warehouse have no display codes, so they add no phantom travel time.
CALL_STAMP=0xffff0858;CALL_TIME=0xffff085a;CALL_STEP=0xffff085c
c.label('lift_call_start36c');c.abs('4a79',0xffff2186);c.branch('6600','lift_call_start_done36c');c.emit('3200');c.abs('3039',0xffff2182);c.abs('9079',0xffff260a);c.emit('3400');c.branch('6600','lift_call_distance36c');wi(CALL_TIME,20);wi(CALL_STEP,20);c.branch('6000','lift_call_stamp36c')
c.label('lift_call_distance36c');c.emit('4a40');c.branch('6a00','lift_call_abs36c');c.emit('4440');c.label('lift_call_abs36c');c.emit('e248c0fc0050');wi(CALL_STEP,80)
# Up (0) is appropriate when target code is lower; down (1) when higher.
c.emit('4a42');c.branch('6b00','lift_call_up36c');c.emit('4a41');c.branch('6600','lift_call_store36c');c.branch('6000','lift_call_wrong36c')
c.label('lift_call_up36c');c.emit('4a41');c.branch('6700','lift_call_store36c')
c.label('lift_call_wrong36c');c.emit('064000a0');wi(CALL_STEP,240)
c.label('lift_call_store36c');c.abs('33c0',CALL_TIME)
c.label('lift_call_stamp36c');c.abs('33f9',0xffff2798);c.long(CALL_STAMP);wi(0xffff2186,1)
c.label('lift_call_start_done36c');c.jump(0x8c54);patch(0x8c4c,'lift_call_start36c',8)
c.label('lift_call_tick36c');c.abs('4a79',0xffff2186);c.branch('6700','lift_call_idle36c');c.abs('3039',0xffff2798);c.abs('9079',CALL_STAMP);c.abs('33f9',0xffff2798);c.long(CALL_STAMP);c.abs('b079',CALL_TIME);c.branch('6400','lift_call_arrive36c');c.abs('9179',CALL_TIME);c.abs('9179',CALL_STEP);c.branch('6e00','lift_call_wait36c');wi(CALL_STEP,80)
c.abs('3039',0xffff260a);c.abs('b079',0xffff2182);c.branch('6700','lift_call_wait36c');c.branch('6d00','lift_call_move_down36c');c.emit('5540');c.branch('6000','lift_call_display36c');c.label('lift_call_move_down36c');c.emit('5440');c.label('lift_call_display36c');c.abs('33c0',0xffff260a)
c.label('lift_call_wait36c');c.jump(0x8b74)
c.label('lift_call_arrive36c');c.abs('4279',0xffff2186);c.abs('4279',CALL_TIME);c.abs('33f9',0xffff2182);c.long(0xffff260a);c.jump(0x8b2a)
c.label('lift_call_idle36c');c.jump(0x8b5c);patch(0x8b18,'lift_call_tick36c')
