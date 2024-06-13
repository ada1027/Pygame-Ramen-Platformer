import pygame

#button class
class Button():
	def __init__(self, x, y, width, height, color_light, color_dark, text, sizeText, text_center_x, text_center_y):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color_light = color_light
		self.color_dark = color_dark
		self.clicked = False
		smallfont = pygame.font.SysFont('Corbel',sizeText,bold=True)
		self.text = smallfont.render(text , True , (255,255,255))
		self.text_center_x = text_center_x
		self.text_center_y = text_center_y
		

	def draw(self, surface):
		#get mouse position
		pos = pygame.mouse.get_pos()

		if self.x <= pos[0] <= self.x+self.width and self.y <= pos[1] <= self.y+self.height:
			pygame.draw.rect(surface,self.color_light,[self.x,self.y,self.width,self.height])
		else:
			pygame.draw.rect(surface,self.color_dark,[self.x,self.y,self.width,self.height])

		surface.blit(self.text, (self.x + self.text_center_x, self.y + self.text_center_y))
		
	def check_for_input(self,pos):
		if self.x <= pos[0] <= self.x+self.width and self.y <= pos[1] <= self.y+self.height:
			return True
		return False