% База знаний по игре Clash Royale

% Редкость
rarity("Common").
rarity("Rare").
rarity("Epic").
rarity("Legendary").

% Тип карты
type("Troops").
type("Buildings").
type("Spells").

% Размещение
placement("Ground").
placement("Air").
placement("Magic").

% Цели
target("Ground").
target("All").
target("Buildings").

% Карты
card("Archers").
card("Baby Dragon").
card("Balloon").
card("Giant").
card("Minions").
card("Prince").
card("Sparky").
card("Cannon").
card("Inferno Tower").
card("Rage").
card("Zap").

% Редкость карты
cardRarity("Archers", "Common").
cardRarity("Baby Dragon", "Epic").
cardRarity("Balloon", "Epic").
cardRarity("Giant", "Rare").
cardRarity("Minions", "Common").
cardRarity("Prince", "Epic").
cardRarity("Sparky", "Legendary").
cardRarity("Cannon", "Common").
cardRarity("Inferno Tower", "Rare").
cardRarity("Rage", "Epic").
cardRarity("Zap", "Common").

% Тип карт
cardType("Archers", "Troops").
cardType("Baby Dragon", "Troops").
cardType("Balloon", "Troops").
cardType("Giant", "Troops").
cardType("Minions", "Troops").
cardType("Prince", "Troops").
cardType("Sparky", "Troops").
cardType("Cannon", "Buildings").
cardType("Inferno Tower", "Buildings").
cardType("Rage", "Spells").
cardType("Zap", "Spells").

% Размещение карт
cardPlacement("Archers", "Ground").
cardPlacement("Baby Dragon", "Air").
cardPlacement("Balloon", "Air").
cardPlacement("Giant", "Ground").
cardPlacement("Minions", "Air").
cardPlacement("Prince", "Ground").
cardPlacement("Sparky", "Ground").
cardPlacement("Cannon", "Ground").
cardPlacement("Inferno Tower", "Ground").
cardPlacement("Rage", "Magic").
cardPlacement("Zap", "Magic").

% Цели, которые карта будет атаковать
cardTarget("Archers", "All").
cardTarget("Baby Dragon", "All").
cardTarget("Balloon", "Buildings").
cardTarget("Giant", "Buildings").
cardTarget("Minions", "All").
cardTarget("Prince", "Ground").
cardTarget("Sparky", "Ground").
cardTarget("Cannon", "Ground").
cardTarget("Inferno Tower", "All").
cardTarget("Rage", "All").
cardTarget("Zap", "All").

% Стоимость карт
cardCost("Archers", 3).
cardCost("Baby Dragon", 4).
cardCost("Balloon", 5).
cardCost("Giant", 5).
cardCost("Minions", 3).
cardCost("Prince", 5).
cardCost("Sparky", 6).
cardCost("Cannon", 3).
cardCost("Inferno Tower", 5).
cardCost("Rage", 2).
cardCost("Zap", 2).



% Правила

% Проверка, может ли карта атаковать другую карту
canAttack(Card1, Card2) :-
    card(Card1), card(Card2),
    (
        cardType(Card2, "Buildings"), card(Card1);
        cardType(Card2, "Troops"), (cardTarget(Card1, "All"); cardPlacement(Card2, "Ground"), cardTarget(Card1, "Ground"))
    ).

% Проверка, сможет карта отвлечь от нападения (отвлечь внимание на себя)
canDefense(Def, Attack) :-
    card(Def), card(Attack), not(cardType(Attack, "Spells")),
    (
        (
            cardType(Def, "Buildings"), cardTarget(Attack, "Buildings");
            not(cardTarget(Attack, "Buildings"));
            cardType(Def, "Spells")
        )
    -> true ; false
    ).

% Проверка, что одна карта дешевле другой
cheaperOrEq(Card1, Card2) :-
    card(Card1), card(Card2),
    (
        (
            cardCost(Card1, Cost1),
            cardCost(Card2, Cost2),
            Cost1 =< Cost2
        )
    -> true ; false
    ).

% Проверка, что мы сможем контратаковать (контратаковать - значит атаковать, а потом пойти в наступление)
canCounterattack(Def, Att) :-
    card(Def), card(Att), not(cardType(Def, "Spells"); cardType(Def, "Buildings"); cardType(Att, "Spells")),
    (
        canAttack(Def, Att)
    -> true; false
    ).

% Проверка, что нам выгодно отвлекать внимание (карта для отвлечения внимания не дороже нападающей карты)
profitableToDistract(Def, Att) :-
    card(Def), card(Att), not(cardType(Att, "Spells")),
    (
        canDefense(Def, Att),
        cheaperOrEq(Def, Att)
    -> true; false
    ).
