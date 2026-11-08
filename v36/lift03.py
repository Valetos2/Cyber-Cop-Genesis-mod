# Display codes increase DOWN:5F..G,L1..L8; Parking/Warehouse excluded.
CALL_STAMP=0xffff0858;CALL_TIME=0xffff085a;CALL_STEP=0xffff085c;CALL_WAYPOINT=0xffff085e
c.label('lift_call_start36c');c.abs('4a79',0xffff2186);c.branch('6600','lift_call_start_done36c');c.emit('3200');c.abs('3039',0xffff2182);c.abs('33c0',CALL_WAYPOINT);c.abs('9079',0xffff260a);c.emit('3400');c.branch('6600','lift_call_distance36c');wi(CALL_TIME,80);c.branch('6000','lift_call_stamp36c')
c.label('lift_call_distance36c');c.emit('4a40');c.branch('6a00','lift_call_abs36c');c.emit('4440');c.label('lift_call_abs36c');c.emit('e248c0fc0050')
c.emit('4a42');c.branch('6b00','lift_call_up36c');c.emit('4a41');c.branch('6600','lift_call_store36c');c.branch('6000','lift_call_wrong36c')
c.label('lift_call_up36c');c.emit('4a41');c.branch('6700','lift_call_store36c')
# Wrong direction: complete the trip to that end of the building, then return.
c.label('lift_call_wrong36c');c.emit('4a41');c.branch('6600','lift_call_detour_down36e');wi(CALL_WAYPOINT,0);c.abs('3039',0xffff260a);c.abs('d079',0xffff2182);c.branch('6000','lift_call_detour_time36e')
c.label('lift_call_detour_down36e');wi(CALL_WAYPOINT,26);c.emit('303c0034');c.abs('9079',0xffff260a);c.abs('9079',0xffff2182)
c.label('lift_call_detour_time36e');c.emit('e248c0fc0050')
c.label('lift_call_store36c');c.abs('33c0',CALL_TIME)
c.label('lift_call_stamp36c');wi(CALL_STEP,80);c.abs('33f9',0xffff2798);c.long(CALL_STAMP);wi(0xffff2186,1)
c.label('lift_call_start_done36c');c.jump(0x8c54);patch(0x8c4c,'lift_call_start36c',8)
c.label('lift_call_tick36c');c.abs('4a79',0xffff2186);c.branch('6700','lift_call_idle36c');c.abs('3039',0xffff2798);c.abs('9079',CALL_STAMP);c.abs('33f9',0xffff2798);c.long(CALL_STAMP);c.abs('b079',CALL_TIME);c.branch('6400','lift_call_arrive36c');c.abs('9179',CALL_TIME);c.abs('9179',CALL_STEP);c.branch('6e00','lift_call_wait36c')
c.label('lift_call_step36e');c.emit('06790050');c.long(CALL_STEP)
c.abs('3039',0xffff260a);c.abs('b079',CALL_WAYPOINT);c.branch('6600','lift_call_move36e');c.abs('33f9',0xffff2182);c.long(CALL_WAYPOINT)
c.label('lift_call_move36e');c.abs('b079',CALL_WAYPOINT);c.branch('6700','lift_call_after_step36e');c.branch('6d00','lift_call_move_down36c');c.emit('5540');c.branch('6000','lift_call_display36c');c.label('lift_call_move_down36c');c.emit('5440');c.label('lift_call_display36c');c.abs('33c0',0xffff260a)
c.label('lift_call_after_step36e');c.abs('4a79',CALL_STEP);c.branch('6f00','lift_call_step36e')
c.label('lift_call_wait36c');c.jump(0x8b74)
c.label('lift_call_arrive36c');c.abs('4279',0xffff2186);c.abs('4279',CALL_TIME);c.abs('33f9',0xffff2182);c.long(0xffff260a);c.jump(0x8b2a)
c.label('lift_call_idle36c');c.jump(0x8b5c);patch(0x8b18,'lift_call_tick36c')
# Ignore the action BEFORE native code can latch another button's texture.
c.label('lift_call_guard36e');c.abs('4a79',0xffff2186);c.branch('6600','lift_call_guard_done36e');c.emit(src[0x8c36:0x8c38].hex());c.branch('6600','lift_call_guard_down36e');wi(0xffff7e30,0xc1);c.jump(0x8c4c)
c.label('lift_call_guard_down36e');c.jump(0x8c44);c.label('lift_call_guard_done36e');c.emit('4e75');patch(0x8c36,'lift_call_guard36e',12)
# Extra mouse presses are visual only. Temporarily overlay held texture and
# restore the latched first-call pair after native framebuffer rendering.
c.label('lift_feedback36e');c.emit('48e7fffe');c.abs('2f39',0xffff7e30)
c.abs('4a79',P);c.branch('6700','lift_feedback_render36e');c.emit('0cb9000058a0');c.long(N+40);c.branch('6600','lift_feedback_render36e')
bi(0xffff2700,255);c.abs('4a79',N+12);c.branch('6700','lift_feedback_render36e');c.emit('08390000');c.long(N+13);c.branch('6700','lift_feedback_render36e');c.call(S['owned_hover04']);c.emit('4a40');c.branch('6700','lift_feedback_render36e')
c.emit('0cb900005954');c.long(N+20);c.branch('6600','lift_feedback_down36e');wi(0xffff7e30,0xc1);c.branch('6000','lift_feedback_render36e')
c.label('lift_feedback_down36e');c.emit('0cb900005968');c.long(N+20);c.branch('6600','lift_feedback_render36e');wi(0xffff7e32,0xc2)
c.label('lift_feedback_render36e');c.call(S['panel_render06']);c.abs('23df',0xffff7e30);c.emit('4cdf7fff4e75');patch(0x38c8,'lift_feedback36e')
