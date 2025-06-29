def build_frames():
    frames = []
    for i in range(123):
        frames.append(())
    horror = ("FIN", 13) # 123 - 158
    for i in range(123, 158):
        frames.append(horror)
    for i in range(158, 193):
        frames.append(())
    hero = ("FIN", 6) # 193 - 200
    for i in range(193, 200):
        frames.append(hero)
    for i in range(200, 241):
        frames.append(())
    summon_choco_mog = ("FIN", 35) # 241 - 262
    for i in range(241, 262):
        frames.append(summon_choco_mog)
    for i in range(262, 269):
        frames.append(())
    item_shopkeep = ("FIN", 142) # 269 - 289
    for i in range(269, 289):
        frames.append(item_shopkeep)
    for i in range(289, 297):
        frames.append(())
    malboro = ("FIN", 106) # 297 - 317
    for i in range(297, 317):
        frames.append(malboro)
    for i in range(317, 322):
        frames.append(())
    rook_turret = ("FIN", 69) # 322 - 340
    for i in range(322, 340):
        frames.append(rook_turret)
    for i in range(340, 351):
        frames.append(())
    bards_bow = ("FIN", 174) # 351 - 370
    for i in range(351, 370):
        frames.append(bards_bow)
    for i in range(370, 379):
        frames.append(())
    hill_gigas = ("FIN", 141) # 379 - 398
    for i in range(379, 398):
        frames.append(hill_gigas)
    for i in range(398, 406):
        frames.append(())
    world_map = ("FIN", 270) # 406 - 428
    for i in range(406, 428):
        frames.append(world_map)
    for i in range(428, 440):
        frames.append(())
    catuar = ("FIN", 177) # 440 - 462
    for i in range(440, 462):
        frames.append(catuar)
    for i in range(462, 483):
        frames.append(())
    garnet = ("FIN", 222) # 483 - 511
    for i in range(483, 511):
        frames.append(garnet)
    for i in range(511, 525):
        frames.append(())
    relentless_x_atm092 = ("FIN", 268) # 525 - 549
    for i in range(525, 549):
        frames.append(relentless_x_atm092)
    for i in range(549, 557):
        frames.append(())
    samuaris_katana = ("FIN", 154) # 557 - 580
    for i in range(557, 580):
        frames.append(samuaris_katana)
    for i in range(580, 587):
        frames.append(())
    tella = ("FIN", 244) # 587 - 613
    for i in range(587, 613):
        frames.append(tella)
    for i in range(613, 628):
        frames.append(())
    magitek_armour = ("FIN", 24) # 628 - 642 foil
    for i in range(628, 642):
        frames.append(magitek_armour)
    for i in range(642, 655):
        frames.append(())
    plans = ("FIN", 294) # 655 - 690
    for i in range(655, 691):
        frames.append(plans)
    return frames

def test_frame_length():
    frames = build_frames()
    assert len(frames) == 690, f"Expected 690 frames, got {len(frames)}"