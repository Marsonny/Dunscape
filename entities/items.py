from utils.validators import validate_if_string, validate_if_number
from utils.exceptions import SaveDataError

class Item:

    def __init__(self, name, description, item_type):
            
        self.name = validate_if_string(name, "name", "Item")
        self.description = validate_if_string(description, "description", "Item")
        self.type = validate_if_string(item_type, "item_type", "Item")
    
    def to_dict(self):
        return {
            "class" : self.__class__.__name__,
            "name"  : self.name,
            "description": self.description,
            "type": self.type
        } 
    
    @classmethod
    def from_dict(cls, data):
        class_name = data.get('class')
        
        # This is the key: we check the stored class name to decide which
        # object to build.
        if class_name == 'Weapon':
            return Weapon(data['name'], data['description'], data['type'], data['weaponDamage'], data['durability'])
        elif class_name == 'Tool':
            return Tool(data['name'], data['description'], data['type'], data['ability'])
        elif class_name == 'Consumable':
            return Consumable(data['name'], data['description'], data['type'], data['effect'])
        else:
            # We use our custom exception here!
            raise SaveDataError(f"Unknown item class in save data: {class_name}")
    
class Weapon(Item):
    def __init__(self, name, description, item_type, weaponDamage, durability):
        super().__init__(name, description, item_type)
        
        self.weaponDamage = validate_if_number(weaponDamage, "weaponDamage", "Weapon")
        self.durability = validate_if_number(durability, "durability", "Weapon")
        
    def to_dict(self):
        weaponData = super().to_dict()
        
        weaponData.update({
            "weaponDamage" : self.weaponDamage,
            "durability": self.durability
        })
        return weaponData
    
class Tool(Item):
    def __init__(self, name, description, item_type, ability):
        super().__init__(name, description, item_type)
        
        self.ability = validate_if_string(ability, "ability", "Tool")
    
    def to_dict(self): 
        toolData = super().to_dict()
        
        toolData.update({
            "ability" : self.ability,
        })
        return toolData
    
class Consumable(Item):
    def __init__(self, name, description, item_type, effect):
        super().__init__(name, description, item_type)
        
        self.effect = validate_if_number(effect, "effect", "Consumable")
        
    def to_dict(self):
        consumableData = super().to_dict()
        
        consumableData.update({
            "effect" : self.effect
        })
        return consumableData