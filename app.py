import streamlit as st
import pandas as pd
import random
import math

# ==========================================
# 1. 게임 기본 세팅 및 데이터 로드 (매운맛 난이도)
# ==========================================
st.set_page_config(page_title="푸드트럭 워즈", layout="centered", page_icon="🚚")

MENUS = {
    "수제버거": {"price": 8000, "cost": 4000, "base_q": 20},
    "타코&핫도그": {"price": 5000, "cost": 2500, "base_q": 40},
    "마라N떡볶이": {"price": 5000, "cost": 2000, "base_q": 35},
    "닭꼬치": {"price": 4000, "cost": 1500, "base_q": 45},
    "슬러시와소다팝": {"price": 2000, "cost": 500, "base_q": 50},
    "알래스카커피": {"price": 3000, "cost": 1000, "base_q": 30},
    "멕시칸츄러스": {"price": 3000, "cost": 1000, "base_q": 30}
}

MISSIONS = [
    # 테마 1. 수요의 극단적 변동
    {"title": "초대형 아이돌 콘서트", "news": "🎸 메인 무대 게릴라 콘서트 2시간 진행! 방문객 2배 폭증!", "choices": ["[선제적 가격 인상] 전 메뉴 가격 20% 인상", "[박리다매] 가격 10% 인하로 주문 싹쓸이", "[현상 유지] 기존 가격과 영업 방식 유지"], "multiplier": 2.0},
    {"title": "기상청 기습 호우 예보", "news": "⛈️ 오후 3시부터 집중 호우 예보! 야외 인파가 빠르게 빠져나갑니다.", "choices": ["[조기 마감] 오늘 영업 종료 (재료 내일 이월)", "[눈물의 떨이] 전 품목 30% 파격 세일", "[현상 유지] 기존 가격과 영업 방식 유지"], "multiplier": 0.4},
    {"title": "유원지 패밀리 데이", "news": "👨‍👩‍👧‍👦 어린이 동반 가족 단위 손님 급증! 유원지 분위기가 활기찹니다.", "choices": ["[가족 세트 할인] 가격 10% 인하 전략", "[감성 마케팅] 홍보 풍선 배포 (마케팅 2만원 지출)", "[현상 유지] 기존 가격과 영업 방식 유지"], "multiplier": 1.3},
    {"title": "입장료 기습 인상", "news": "🎫 주최 측의 횡포! 비싼 입장료 탓에 손님들의 지갑이 얇아졌습니다.", "choices": ["[가성비 어필] 전 메뉴 가격 15% 인하", "[고급화 전략] 원가 10% 상승 및 가격 20% 인상", "[현상 유지] 기존 가격과 영업 방식 유지"], "multiplier": 0.7},
    {"title": "유원지 야간 개장", "news": "🌙 오늘 밤 11시까지 연장 영업! 야간 방문객 추가 유입 확정.", "choices": ["[알바 추가 고용] 고정비 5만원 지출 (수요 100% 흡수)", "[야간 떨이 행사] 가격 20% 인하로 회전율 극대화", "[현상 유지] 추가 지출 없이 내 체력껏 영업"], "multiplier": 1.4},
    
    # 테마 2. 공급 및 원가 충격
    {"title": "글로벌 물류 대란", "news": "🚢 물류 대란 발발! 튀김유 및 곡물 도매가가 기습 폭등했습니다.", "choices": ["[선제적 가격 인상] 전 메뉴 가격 20% 인상", "[원가율 방어] 슈링크플레이션/양 줄이기 (수요 10% 이탈)", "[현상 유지] 기존 가격과 레시피 그대로 영업"], "multiplier": 1.0},
    {"title": "축산 농가 파업", "news": "🥩 소고기, 돼지고기, 닭고기 도매가가 무섭게 치솟고 있습니다.", "choices": ["[선제적 가격 인상] 전 메뉴 가격 20% 인상", "[원가 절감] 대체육/저렴한 부위 혼합 (수요 10% 이탈)", "[현상 유지] 기존 가격과 레시피 그대로 영업"], "multiplier": 1.0},
    {"title": "기호식품 원자재 폭등", "news": "☕ 남미 이상 기후로 커피 원두 및 카카오 등 수입 식자재 가격 급등!", "choices": ["[선제적 가격 인상] 전 메뉴 가격 20% 인상", "[원가 절감] 저렴한 재료 혼합 및 시럽 조절 (수요 10% 이탈)", "[현상 유지] 기존 가격과 레시피 그대로 영업"], "multiplier": 1.0},
    {"title": "단수 사태", "news": "🚰 수도관 파열! 식수 및 얼음 수급에 비상이 걸렸습니다.", "choices": ["[생수 긴급 매입] 고정비 3만원 지출로 정상 영업", "[위생 우선] 일회용기 전면 전환 (원가 5% 상승)", "[현상 유지] 남은 물로 최대한 버티며 영업"], "multiplier": 0.8},
    {"title": "최저임금 인상 적용", "news": "📈 오늘부터 파트타임 시급 인상 적용! 인건비 부담이 늘어납니다.", "choices": ["[임금 인상 반영] 전 메뉴 가격 15% 인상", "[1인 운영 체제] 알바 없이 혼자 운영 (수요 20% 감소)", "[현상 유지] 이윤 감소를 감수하고 기존 상태 유지"], "multiplier": 1.0},
    
    # 테마 3. 트렌드 변화와 경쟁
    {"title": "집단 식중독 루머", "news": "🚨 입구 쪽 트럭 구역에서 장염 환자 발생 루머 확산!", "choices": ["[안심 마케팅] 위생 인증서 긴급 부착 (마케팅 2만원 지출)", "[신뢰 회복 할인] 가격 15% 파격 인하", "[현상 유지] 기존 가격과 영업 방식 유지"], "multiplier": 0.6},
    {"title": "대형 편의점 공습", "news": "🍱 유원지 바로 옆 24시간 편의점 오픈! 즉석식품 반값 할인 시작.", "choices": ["[맞불 가격 경쟁] 전 메뉴 가격 20% 인하", "[품질 차별화] 편의점과 차별화된 수제 퀄리티 홍보 (마케팅 2만원 지출)", "[현상 유지] 기존 가격과 영업 방식 유지"], "multiplier": 0.7},
    {"title": "불닭 챌린지 유행", "news": "🌶️ 매운맛 챌린지 전국적 유행! 자극적인 맛을 찾는 손님이 쏟아집니다.", "choices": ["[트렌드 탑승] 유행 맞춤형 스페셜 메뉴 출시 (원가 10% 상승)", "[틈새 시장] 매운맛에 지친 사람 타겟 10% 할인", "[현상 유지] 유행에 흔들리지 않고 기존 메뉴 고수"], "multiplier": 1.3},
    {"title": "인플루언서 극찬", "news": "📸 100만 유튜버가 \"이 유원지는 길거리 음식이 미쳤음\" 영상 업로드!", "choices": ["[가격 인상] 수요 폭증에 맞춰 가격 15% 인상", "[인증마크 홍보] 유튜버 방문 포스터 부착 (마케팅 1만원 지출)", "[현상 유지] 기존 가격과 영업 방식 유지"], "multiplier": 1.6},
    {"title": "다이어트 열풍", "news": "🥗 건강 프로그램 방영 후, 길거리 고칼로리 음식 기피 현상 발생!", "choices": ["[헬시 옵션 도입] 라이트 재료 도입 (원가 15% 상승)", "[감성 마케팅] 스트레스 해소 맛 강조 홍보 (마케팅 2만원 지출)", "[현상 유지] 기존 가격과 영업 방식 유지"], "multiplier": 0.7},
    
    # 테마 4. 거시 환경 및 돌발 변수
    {"title": "역대급 폭염 경보", "news": "🥵 가만히 있어도 숨이 막히는 폭염! 야외활동 자제 경보 발령!!", "choices": ["[눈물의 떨이] 전 품목 30% 파격 세일", "[조기 마감] 오늘 영업은 여기서 종료 (남은 재료 내일 이월)", "[현상 유지] 기존 가격과 영업 방식 유지"], "multiplier": 0.2},
    {"title": "상인회 가격 담합", "news": "🤝 상인회장 긴급 지시: \"전 메뉴 가격 20% 올립시다! 배신 금지!\"", "choices": ["[의리 지키기] 단체 협약에 따라 가격 20% 인상", "[눈치 작전] 의리는 지키되 생색내기용 10%만 인상", "[현상 유지] 담합을 은밀하게 배신하고 기존 가격 고수"], "multiplier": 1.0},
    {"title": "쓰레기통 대란", "news": "🗑️ 쓰레기통 포화 및 악취 민원 발생! 손님들이 불쾌감을 느낍니다.", "choices": ["[클린 존 마케팅] 트럭 앞 청소 알바 고용 (고정비 5만원 지출)", "[친환경 캠페인] 수거용 친환경 패키지 전환 (원가 10% 상승)", "[현상 유지] 내 트럭 내부만 관리하고 기존 방식 고수"], "multiplier": 0.7},
    {"title": "악의적 루머", "news": "📱 지역 커뮤니티카페에 \"푸드트럭들 화학 조미료 범벅이래요\" 루머 확산!", "choices": ["[안심 해명] 안내문 제작 (마케팅 3만원 지출)", "[억울하니까 세일] 루머 돌파용 가격 20% 파격 인하", "[현상 유지] 선동에 흔들리지 않고 기존 방식대로 영업"], "multiplier": 0.5},
    {"title": "청년 지원금 배포", "news": "💸 유원지 방문객 전원에게 '푸드트럭 전용 5,000원 쿠폰' 지급 완료!", "choices": ["[쿠폰 특수] 가격 15% 인상으로 마진 극대화", "[쿠폰 시너지 할인] 가격 10% 인하로 손님 싹쓸이", "[현상 유지] 평소와 다름없이 기존 가격 고수"], "multiplier": 1.5},
    {"title": "원산지 특별 단속", "news": "🕵️ 유원지 불량 식자재 특별 단속 실시! 고객들의 의심이 커집니다.", "choices": ["[인증 마케팅] 원산지 인증판 부착 (마케팅 2만원 지출)", "[안심 할인] 단속 기간 맞이 10% 가격 인하", "[현상 유지] 원래 정품 재료이므로 기존 방식 고수"], "multiplier": 0.8},
    {"title": "발전기 화재", "news": "🚒 건너편 B구역 트럭 전면 영업 중단! 우리 구역으로 손님이 쏟아집니다.", "choices": ["[독점력 행사] 가격 30% 기습 인상", "[착한 마케팅] 대피 손님 환대 안내문 부착 (마케팅 1만원 지출)", "[현상 유지] 동요하지 않고 평소 가격 고수"], "multiplier": 1.8},
    {"title": "스폰서 음료 배포", "news": "🥤 대기업 홍보 부스에서 생수와 캔콜라를 전원 무료 배포합니다!", "choices": ["[단품 집중 할인] 가격 20% 인하 전략", "[사이드 메뉴 강화] 결합 마케팅 (마케팅 2만원 지출)", "[현상 유지] 가격 및 마케팅 변동 없이 고수"], "multiplier": 1.0},
    {"title": "학교 단체 소풍", "news": "🎒 근처 중·고등학교에서 학생 500명이 단체 소풍을 왔습니다!", "choices": ["[학생 특별 할인] 가격 15% 인하로 학생층 흡수", "[전투 영업] 빠른 회전율을 위한 임시 알바 고용 (고정비 5만원 지출)", "[현상 유지] 평소 가격과 인원으로 영업"], "multiplier": 1.7},
    {"title": "불꽃놀이 피날레", "news": "🎆 유원지 메인 불꽃놀이! 역대 최고 인파가 단 1시간 동안 몰립니다.", "choices": ["[피날레 특수] 가격 40% 대폭 인상", "[박리다매 스퍼트] 가격 20% 인하로 회전율 극대화", "[현상 유지] 유종의 미를 거두며 기존 가격 고수"], "multiplier": 2.5}
]

# ==========================================
# 2. 전역 상태 관리
# ==========================================
@st.cache_resource
def get_db():
    return {
        "users": {},           
        "phase": "대기실",       
        "day": 1,              
        "mission": None,       
        "mission_pool": random.sample(MISSIONS, len(MISSIONS))
    }

db = get_db()

if "nickname" not in st.session_state:
    st.session_state.nickname = None
if "my_phase" not in st.session_state:
    st.session_state.my_phase = "대기실"

# ==========================================
# 3. 로그인 
# ==========================================
def render_login():
    st.title("🚚 푸드트럭 워즈")
    st.write("보이지 않는 손의 선택! 유원지 생존 게임에 오신 사장님 환영합니다.")
    
    tab1, tab2 = st.tabs(["사장님(학생) 입장", "관리자(교수님) 입장"])
    
    with tab1:
        with st.form("student_login_form"):
            nick = st.text_input("닉네임 (7글자 이내)", max_chars=7)
            menu = st.selectbox("판매할 메뉴 선택", list(MENUS.keys()))
            init_inv = st.selectbox("첫날 준비할 인분 수", [30, 50, 70, 100])
            submit = st.form_submit_button("영업 준비 완료")
            
            if submit:
                if not nick.strip():
                    st.error("닉네임을 입력하세요!")
                elif nick == "admin":
                    st.error("이 닉네임은 사용할 수 없습니다.")
                elif nick in db["users"]:
                    st.session_state.nickname = nick
                    st.rerun()
                else:
                    # [수정] 첫 발주 물류비 30,000원 반영
                    init_cost = init_inv * MENUS[menu]["cost"] + 30000
                    db["users"][nick] = {
                        "menu": menu,
                        "cash": 1000000 - init_cost,
                        "inventory": init_inv,
                        "day_ready": False,
                        "night_ready": False,
                        "last_receipt": None
                    }
                    st.session_state.nickname = nick
                    st.rerun()

    with tab2:
        with st.form("admin_login_form"):
            admin_id = st.text_input("관리자 ID")
            admin_pw = st.text_input("비밀번호", type="password")
            admin_submit = st.form_submit_button("통제 센터 접속")
            
            if admin_submit:
                if admin_id == "admin" and admin_pw == "2556":
                    st.session_state.nickname = "admin"
                    st.rerun()
                else:
                    st.error("ID 또는 비밀번호가 일치하지 않습니다.")

# ==========================================
# 4. 게임 메인 화면 (학생 시점)
# ==========================================
def render_student_view():
    nick = st.session_state.nickname
    user_data = db["users"].get(nick)
    
    if not user_data:
        st.session_state.nickname = None
        st.rerun()

    if st.session_state.my_phase != db["phase"]:
        st.info("🔔 관리자가 새로운 단계를 열었습니다!")
        if db["phase"] == "낮":
            if st.button("🌅 아침 맞이하기 (새 미션 확인)", use_container_width=True, type="primary"):
                st.session_state.my_phase = "낮"
                st.rerun()
        elif db["phase"] == "밤":
            if st.button("🌙 정산 결과 확인 (영수증 보기)", use_container_width=True, type="primary"):
                st.session_state.my_phase = "밤"
                st.rerun()
        elif db["phase"] == "종료":
            if st.button("🏆 최종 랭킹 확인", use_container_width=True, type="primary"):
                st.session_state.my_phase = "종료"
                st.rerun()
        elif db["phase"] == "대기실":
            if st.button("🔄 게임 초기화 됨 (처음으로)", use_container_width=True):
                st.session_state.my_phase = "대기실"
                st.rerun()
        return

    st.header(f"사장님: {nick}")
    st.write(f"**메뉴:** {user_data['menu']} | **💰 자본금:** {user_data['cash']:,}원 | **📦 재고:** {user_data['inventory']}인분")
    st.divider()

    if st.session_state.my_phase == "대기실":
        st.info("⏳ 영업 준비 완료! 모든 사장님이 입장하고 게임이 시작될 때까지 대기해 주세요.")
        if st.button("🔄 게임 시작 확인 (새로고침)", use_container_width=True):
            st.rerun()

    elif st.session_state.my_phase == "낮":
        if user_data["day_ready"]:
            st.success("✔️ 영업 전략 제출 완료! 관리자의 정산(밤)을 기다리세요.")
            if st.button("🔄 정산 완료 확인 (새로고침)", use_container_width=True):
                st.rerun()
                
        elif user_data["inventory"] <= 0:
            st.subheader("🚨 긴급 상황: 재고가 모두 소진되었습니다!")
            st.error("창고가 완전히 비어 있어 오늘 정상적인 뉴스 미션에 참가할 수 없습니다. 대책을 수립하세요.")
            
            with st.form("emergency_form"):
                emergency_choice = st.radio(
                    "재고 고갈 대책 선택",
                    [
                        "🛏️ [강제 휴업] 오늘 하루 영업을 쉬고 트럭을 정비합니다. (오늘 매출 0원, 기본 자리세 50,000원 납부)",
                        "🚚 [긴급 퀵 배송] 퀵 배송비 100,000원을 내고 재료 50인분을 긴급 공수하여 미션에 참여합니다."
                    ]
                )
                submit = st.form_submit_button("결정 제출")
                if submit:
                    if "긴급 퀵 배송" in emergency_choice:
                        # [수정] 긴급 퀵 배송비 100,000원 적용
                        if user_data["cash"] < 100000:
                            st.error("❌ 잔액이 부족하여 퀵 배송을 이용할 수 없습니다. 강제 휴업을 선택하세요.")
                        else:
                            db["users"][nick]["cash"] -= 100000
                            db["users"][nick]["inventory"] = 50
                            db["users"][nick]["day_choice"] = "[현상 유지] 기존 가격과 영업 방식 유지" if db["day"] > 1 else "[현상 유지] 정가 영업"
                            db["users"][nick]["day_ready"] = True
                            st.rerun()
                    else:
                        db["users"][nick]["day_choice"] = "[강제 휴업]"
                        db["users"][nick]["day_ready"] = True
                        st.rerun()
        else:
            if db["day"] == 1:
                st.subheader("🌅 [1일 차] 두근두근 첫 장사!")
                st.info("오늘은 특별한 뉴스 속보가 없는 맑고 평범한 하루입니다. 기본 전략을 선택하세요.")
                options = ["프리미엄 전략 (가격 10% 인상)", "홍보 세일 (가격 10% 인하)", "[현상 유지] 정가 영업"]
            else:
                m = db["mission"]
                st.subheader(f"🌅 [{db['day']}일 차] 오늘의 속보")
                st.error(m["news"])
                options = m["choices"]
            
            with st.form("day_form"):
                choice = st.radio("오늘의 영업 전략", options)
                submit = st.form_submit_button("최종 결정 (제출 후 수정 불가)")
                if submit:
                    db["users"][nick]["day_choice"] = choice
                    db["users"][nick]["day_ready"] = True
                    st.rerun()

    elif st.session_state.my_phase == "밤":
        if user_data["night_ready"]:
            st.success("✔️ 야간 발주 완료! 주무시면서 내일 아침을 기다리세요.")
            if st.button("🔄 다음 날 시작 확인 (새로고침)", use_container_width=True):
                st.rerun()
        else:
            st.subheader(f"🌙 [{db['day']}일 차] 마감 영수증")
            receipt = user_data["last_receipt"]
            
            st.write(f"✅ **판매 수량:** {receipt['sold']}인분 (찾아온 손님: {receipt['demand']}명)")
            st.write(f"➕ **매출액:** {receipt['revenue']:,}원")
            st.write(f"➖ **고정비(자리세/마케팅/인건비):** {receipt['fixed_cost']:,}원")
            st.info(f"**최종 잔고:** {user_data['cash']:,}원")
            
            st.divider()
            st.subheader("🚚 내일 장사 도매상 발주")
            menu_cost = MENUS[user_data["menu"]]["cost"]
            # [수정] 일반 발주 배달비 30,000원 표시
            st.write(f"*(내 메뉴 원가: {menu_cost:,}원 / 1회 배달비: 30,000원)*")
            
            with st.form("order_form"):
                order_qty = st.selectbox("추가 발주 인분 수", [0, 30, 50, 70, 100])
                # [수정] 발주 시 고정 물류비 30,000원 적용
                total_cost = (order_qty * menu_cost) + 30000 if order_qty > 0 else 0
                st.write(f"**총 예상 비용: {total_cost:,}원**")
                
                submit = st.form_submit_button("발주서 확정 (제출)")
                
                if submit:
                    if user_data["inventory"] + order_qty > 100:
                        st.error("❌ 창고 최대 한도(100인분)를 초과할 수 없습니다.")
                    elif user_data["cash"] < total_cost:
                        st.error("❌ 자본금이 부족합니다! (수량 하향 또는 발주 안 함[0인분] 선택)")
                    else:
                        db["users"][nick]["cash"] -= total_cost
                        db["users"][nick]["inventory"] += order_qty
                        db["users"][nick]["night_ready"] = True
                        st.rerun()

    elif st.session_state.my_phase == "종료":
        st.balloons()
        st.subheader("🎉 푸드트럭 워즈 영업 종료!")
        st.write(f"최종 자본금: **{user_data['cash']:,}원**")
        st.success("대단히 수고하셨습니다. 화면의 최종 랭킹을 확인하세요!")

# ==========================================
# 5. 관리자 통제 센터
# ==========================================
def render_admin():
    st.header("👨‍🏫 관리자 통제 센터")
    
    if st.button("🔄 실시간 현황 업데이트 (새로고침)", type="secondary"):
        st.rerun()
    
    total_users = len(db["users"])
    ready_users = sum(1 for u in db["users"].values() if (u["day_ready"] if db["phase"] == "낮" else u["night_ready"]))
    
    col1, col2, col3 = st.columns(3)
    col1.metric("현재 페이즈", f"[{db['day']}일 차] {db['phase']}")
    col2.metric("접속한 사장님", f"{total_users} 명")
    col3.metric("제출 완료", f"{ready_users} 명")
    st.divider()

    st.subheader("🎮 게임 진행 컨트롤")
    
    if db["phase"] in ["대기실", "밤"]:
        if st.button("🌅 다음 날 아침 맞이 (새 미션 발동)", type="primary"):
            if db["phase"] == "밤":
                db["day"] += 1
                if not db["mission_pool"]:
                    db["mission_pool"] = random.sample(MISSIONS, len(MISSIONS))
                db["mission"] = db["mission_pool"].pop()
                
            db["phase"] = "낮"
            for u in db["users"].values():
                u["day_ready"] = False
            st.rerun()

    if db["phase"] == "낮":
        if st.button("📊 낮 영업 마감 및 영수증 정산", type="primary"):
            for nick, data in db["users"].items():
                m_info = MENUS[data["menu"]]
                base_demand = m_info["base_q"]
                base_price = m_info["price"]
                
                multiplier = db["mission"]["multiplier"] if db["day"] > 1 else 1.0
                
                choice_str = str(data.get("day_choice", ""))
                mod_price = 1.0
                mod_demand = 1.0
                # [수정] 기본 자리세 50,000원 상향
                extra_fc = 50000 
                
                if "가격 10% 인상" in choice_str: mod_price = 1.1; mod_demand = 0.85
                elif "가격 15% 인상" in choice_str: mod_price = 1.15; mod_demand = 0.8
                elif "가격 20% 인상" in choice_str: mod_price = 1.2; mod_demand = 0.7
                elif "가격 30% 인상" in choice_str: mod_price = 1.3; mod_demand = 0.5
                elif "가격 40% 인상" in choice_str: mod_price = 1.4; mod_demand = 0.4
                elif "가격 10% 인하" in choice_str: mod_price = 0.9; mod_demand = 1.3
                elif "가격 15% 인하" in choice_str: mod_price = 0.85; mod_demand = 1.5
                elif "가격 20% 인하" in choice_str: mod_price = 0.8; mod_demand = 1.8
                elif "가격 30% 인하" in choice_str: mod_price = 0.7; mod_demand = 2.5
                
                # [수정] 마케팅비 및 인건비(5만) 동적 파싱 추가
                if "마케팅" in choice_str or "지출" in choice_str or "고용" in choice_str or "매입" in choice_str:
                    if "1만원" in choice_str: extra_fc += 10000; mod_demand *= 1.3
                    elif "2만원" in choice_str: extra_fc += 20000; mod_demand *= 1.6
                    elif "3만원" in choice_str: extra_fc += 30000; mod_demand *= 1.9
                    elif "5만원" in choice_str: extra_fc += 50000; mod_demand *= 2.0
                
                if "이탈" in choice_str or "감소" in choice_str:
                    if "10%" in choice_str: mod_demand *= 0.9
                    if "20%" in choice_str: mod_demand *= 0.8
                
                final_demand = math.floor(base_demand * multiplier * mod_demand)
                final_price = math.floor(base_price * mod_price)
                
                sold = min(final_demand, data["inventory"])
                revenue = sold * final_price
                
                # 조기 마감 및 강제 휴업 예외처리 (휴업 시에도 자리세 5만원은 정상 차감됨)
                if "조기 마감" in choice_str or "[강제 휴업]" in choice_str:
                    final_demand = 0
                    sold = 0
                    revenue = 0
                
                data["cash"] += revenue - extra_fc
                data["inventory"] -= sold
                
                data["last_receipt"] = {
                    "demand": final_demand,
                    "sold": sold,
                    "revenue": revenue,
                    "fixed_cost": extra_fc
                }
            
            db["phase"] = "밤"
            for u in db["users"].values():
                u["night_ready"] = False
            st.rerun()

    if st.button("🏆 게임 최종 종료 (시상식)"):
        db["phase"] = "종료"
        st.rerun()
        
    st.divider()
    
    st.subheader("📊 실시간 랭킹")
    if db["users"]:
        df = pd.DataFrame([
            {"닉네임": k, "메뉴": v["menu"], "자본금": f"{v['cash']:,}원", "재고": f"{v['inventory']}인분", "제출여부": "완료" if (v["day_ready"] if db["phase"]=="낮" else v["night_ready"]) else "대기중"} 
            for k, v in db["users"].items()
        ])
        df['자본금_숫자'] = df['자본금'].str.replace('원', '').str.replace(',', '').astype(int)
        df = df.sort_values(by="자본금_숫자", ascending=False).drop(columns=['자본금_숫자']).reset_index(drop=True)
        df.index = df.index + 1
        st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    st.subheader("🚨 비상 통제 구역")
    kick_target = st.selectbox("강제 퇴장시킬 닉네임", ["선택 안함"] + list(db["users"].keys()))
    if st.button("❌ 선택 유저 퇴장") and kick_target != "선택 안함":
        del db["users"][kick_target]
        st.success(f"{kick_target} 퇴장 완료!")
        st.rerun()
        
    if st.button("🔄 전면 초기화 (새 게임)"):
        db["users"].clear()
        db["phase"] = "대기실"
        db["day"] = 1
        db["mission"] = None
        db["mission_pool"] = random.sample(MISSIONS, len(MISSIONS))
        st.success("초기화 완료!")
        st.rerun()

# ==========================================
# 라우팅
# ==========================================
if st.session_state.nickname is None:
    render_login()
elif st.session_state.nickname == "admin":
    render_admin()
else:
    render_student_view()