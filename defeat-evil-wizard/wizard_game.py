import random

# =========================
# Base Character class
# =========================
class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power

        # status effects for abilities
        self.evade_next = False
        self.shield_next = False

    def attack(self, opponent):
        # randomize damage (requirement)
        damage = random.randint(int(self.attack_power * 0.7), int(self.attack_power * 1.1))

        # opponent has evade?
        if getattr(opponent, "evade_next", False):
            opponent.evade_next = False
            print(f"{opponent.name} evades the attack! No damage taken.")
            return

        # opponent has shield?
        if getattr(opponent, "shield_next", False):
            opponent.shield_next = False
            blocked = int(damage * 0.8)
            damage = max(0, damage - blocked)
            print(f"{opponent.name}'s shield blocks {blocked} damage!")

        opponent.health -= damage
        if opponent.health < 0:
            opponent.health = 0

        print(f"{self.name} attacks {opponent.name} for {damage} damage!")

    def heal(self):
        # healing mechanic (requirement)
        amount = random.randint(18, 30)
        before = self.health
        self.health = min(self.max_health, self.health + amount)
        print(f"{self.name} heals for {self.health - before} HP! (Health: {self.health}/{self.max_health})")

    def display_stats(self):
        print(f"\n{self.name}'s Stats")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Attack Power: {self.attack_power}")

    def use_ability(self, choice, opponent):
        # overridden by subclasses
        print("No abilities available.")


# =========================
# Warrior
# =========================
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25)

    def use_ability(self, choice, opponent):
        if choice == "1":
            # Power Strike: big hit
            damage = random.randint(35, 55)
            if opponent.evade_next:
                opponent.evade_next = False
                print(f"{opponent.name} evades your Power Strike!")
                return
            opponent.health = max(0, opponent.health - damage)
            print(f"{self.name} uses POWER STRIKE for {damage} damage!")
        elif choice == "2":
            # Battle Cry: increase next attack power temporarily
            boost = random.randint(8, 15)
            self.attack_power += boost
            print(f"{self.name} uses BATTLE CRY! Attack Power +{boost} for the rest of the fight.")
        else:
            print("Invalid ability choice.")


# =========================
# Mage
# =========================
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)

    def use_ability(self, choice, opponent):
        if choice == "1":
            # Fireball: heavy damage
            damage = random.randint(30, 60)
            if opponent.evade_next:
                opponent.evade_next = False
                print(f"{opponent.name} evades your Fireball!")
                return
            opponent.health = max(0, opponent.health - damage)
            print(f"{self.name} casts FIREBALL for {damage} damage!")
        elif choice == "2":
            # Arcane Shield: blocks next attack (using shield_next flag)
            self.shield_next = True
            print(f"{self.name} casts ARCANE SHIELD! Next incoming attack will be reduced.")
        else:
            print("Invalid ability choice.")


# =========================
# Archer (new class)
# =========================
class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=115, attack_power=28)

    def use_ability(self, choice, opponent):
        if choice == "1":
            # Quick Shot: two smaller hits
            print(f"{self.name} uses QUICK SHOT!")
            for _ in range(2):
                damage = random.randint(12, 22)
                if opponent.evade_next:
                    opponent.evade_next = False
                    print(f"{opponent.name} evades one of the arrows!")
                    continue
                opponent.health = max(0, opponent.health - damage)
                print(f"  Arrow hits for {damage} damage!")
        elif choice == "2":
            # Evade: avoid next attack
            self.evade_next = True
            print(f"{self.name} uses EVADE! Next enemy attack will miss.")
        else:
            print("Invalid ability choice.")


# =========================
# Paladin (new class)
# =========================
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=155, attack_power=20)

    def use_ability(self, choice, opponent):
        if choice == "1":
            # Holy Strike: bonus damage
            damage = random.randint(25, 45)
            if opponent.evade_next:
                opponent.evade_next = False
                print(f"{opponent.name} evades your Holy Strike!")
                return
            opponent.health = max(0, opponent.health - damage)
            print(f"{self.name} uses HOLY STRIKE for {damage} damage!")
        elif choice == "2":
            # Divine Shield: reduce next hit strongly
            self.shield_next = True
            print(f"{self.name} uses DIVINE SHIELD! Next incoming attack will be reduced.")
        else:
            print("Invalid ability choice.")


# =========================
# Evil Wizard
# =========================
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=15)

    def regenerate(self):
        regen = random.randint(5, 12)
        self.health = min(self.max_health, self.health + regen)
        print(f"{self.name} regenerates {regen} health! (Health: {self.health}/{self.max_health})")


# =========================
# Game Functions
# =========================
def create_character():
    print("\nChoose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer")
    print("4. Paladin")

    class_choice = input("Enter the number of your class choice: ").strip()
    name = input("Enter your character's name: ").strip() or "Hero"

    if class_choice == "1":
        return Warrior(name)
    elif class_choice == "2":
        return Mage(name)
    elif class_choice == "3":
        return Archer(name)
    elif class_choice == "4":
        return Paladin(name)
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Warrior(name)


def ability_menu(player):
    print("\nChoose an ability:")
    if isinstance(player, Warrior):
        print("1. Power Strike (big damage)")
        print("2. Battle Cry (increase attack power)")
    elif isinstance(player, Mage):
        print("1. Fireball (high damage)")
        print("2. Arcane Shield (reduce next incoming attack)")
    elif isinstance(player, Archer):
        print("1. Quick Shot (two arrow hits)")
        print("2. Evade (dodge next attack)")
    elif isinstance(player, Paladin):
        print("1. Holy Strike (bonus damage)")
        print("2. Divine Shield (reduce next incoming attack)")
    return input("Enter ability choice: ").strip()


def battle(player, wizard):
    print("\n⚔️  Battle Start!")
    wizard.display_stats()
    player.display_stats()

    while wizard.health > 0 and player.health > 0:
        print("\n--- Your Turn ---")
        print("1. Attack")
        print("2. Use Special Ability")
        print("3. Heal")
        print("4. View Stats")

        choice = input("Choose an action: ").strip()

        if choice == "1":
            player.attack(wizard)
        elif choice == "2":
            abil_choice = ability_menu(player)
            player.use_ability(abil_choice, wizard)
        elif choice == "3":
            player.heal()
        elif choice == "4":
            player.display_stats()
            wizard.display_stats()
            continue
        else:
            print("Invalid choice. Try again.")
            continue

        # check victory after player turn
        if wizard.health <= 0:
            break

        # wizard turn
        print("\n--- Wizard's Turn ---")
        wizard.regenerate()
        wizard.attack(player)

        if player.health <= 0:
            break

    # end messages (requirement)
    if player.health <= 0:
        print(f"\n💀 {player.name} has been defeated! The wizard wins...")
    else:
        print(f"\n🏆 The wizard {wizard.name} has been defeated by {player.name}! You win!")


def main():
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)


if __name__ == "__main__":
    main()
