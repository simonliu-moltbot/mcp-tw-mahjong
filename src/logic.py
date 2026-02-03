
import sys

def calculate_tai(
    melds, 
    eye, 
    hu_tile, 
    is_self_drawn, 
    is_dealer, 
    dealer_count, 
    wind_round, 
    wind_seat, 
    flower_tiles,
    is_last_tile=False,
    is_robbing_kong=False,
    is_kong_on_kong=False
):
    """
    Calculate Tai for Taiwan 16-card Mahjong.
    melds: List of list of strings, e.g., [['1m','1m','1m'], ['2m','3m','4m'], ...]
    eye: List of 2 strings, e.g., ['5m', '5m']
    hu_tile: The tile that finished the hand.
    is_self_drawn: Bool
    is_dealer: Bool
    dealer_count: Int (0 for first time, 1 for consecutive win 1)
    wind_round: String ('東', '南', '西', '北')
    wind_seat: String ('東', '南', '西', '北')
    flower_tiles: List of strings ('f1'..'f8')
    """
    total_tai = 0
    reasons = []

    # 1. 莊家相關
    if is_dealer:
        total_tai += 1
        reasons.append(f"莊家 (+1)")
        if dealer_count > 0:
            tai = dealer_count * 2
            total_tai += tai
            reasons.append(f"連 {dealer_count} 拉 {dealer_count} (+{tai})")
    
    # 2. 自摸
    if is_self_drawn:
        total_tai += 1
        reasons.append("自摸 (+1)")

    # 3. 風牌與花牌
    # 圈風
    for meld in melds:
        if all(tile == wind_round for tile in meld):
            total_tai += 1
            reasons.append(f"圈風 {wind_round} (+1)")
        if all(tile == wind_seat for tile in meld):
            total_tai += 1
            reasons.append(f"門風 {wind_seat} (+1)")
    
    # 三元牌
    dragons = {'中': '紅中', '發': '發財', '白': '白板'}
    dragon_count = 0
    for dragon, name in dragons.items():
        if any(all(tile == dragon for tile in meld) for meld in melds):
            total_tai += 1
            reasons.append(f"{name} (+1)")
            dragon_count += 1
    
    if dragon_count == 3:
        # 大三元 (Already added 3 above, adjust to total 8)
        total_tai += (8 - 3)
        reasons.append("大三元 (補足 8 台)")
    elif dragon_count == 2 and any(all(tile == d for tile in eye) for d in dragons):
        # 小三元 (Already added 2 above, adjust to total 4)
        total_tai += (4 - 2)
        reasons.append("小三元 (補足 4 台)")

    # 花牌 (Simple logic: 1 tai per matching flower)
    # f1-f4: Spring/Summer/Autumn/Winter, f5-f8: Plum/Orchid/Bamboo/Chrysanthemum
    # Seat East: f1, f5; South: f2, f6; West: f3, f7; North: f4, f8
    seat_to_flowers = {'東': ['f1', 'f5'], '南': ['f2', 'f6'], '西': ['f3', 'f7'], '北': ['f4', 'f8']}
    correct_flowers = seat_to_flowers.get(wind_seat, [])
    for f in flower_tiles:
        if f in correct_flowers:
            total_tai += 1
            reasons.append(f"正花 {f} (+1)")
    
    if len(flower_tiles) == 8:
        total_tai += 8
        reasons.append("八仙過海 (+8)")
    elif len(flower_tiles) == 7:
        total_tai += 8
        reasons.append("七搶一 (+8)")

    # 4. 牌型相關 (Simplified checking)
    all_tiles = [t for m in melds for t in m] + eye
    
    # 清一色 / 湊一色
    suits = set()
    has_honor = False
    for t in all_tiles:
        if 'm' in t: suits.add('m')
        elif 's' in t: suits.add('s')
        elif 'p' in t: suits.add('p')
        else: has_honor = True
    
    if len(suits) == 1:
        if has_honor:
            total_tai += 2
            reasons.append("湊一色 (+2)")
        else:
            total_tai += 8
            reasons.append("清一色 (+8)")
    elif len(suits) == 0 and has_honor:
        total_tai += 16
        reasons.append("字一色 (+16)")

    # 碰碰胡
    if all(len(meld) >= 3 and meld[0] == meld[1] == meld[2] for meld in melds):
        total_tai += 4
        reasons.append("碰碰胡 (+4)")

    # 暗刻
    # (Needs information on which melds were concealed/revealed)
    # This calculator assumes melds are what they are. 
    # For simplicity, we might need an 'is_concealed' flag per meld.

    return {
        "total_tai": total_tai,
        "reasons": reasons
    }
