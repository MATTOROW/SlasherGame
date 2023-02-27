# from PIL import Image
#
# im = Image.open('C:/Users/Никита/Documents/IT/python/Ялицей/SlasherGame/sprites/player/3x/vagabond-dash.gif')
#
# def iter_frames(im):
#     try:
#         i= 0
#         while 1:
#             im.seek(i)
#             imframe = im.copy()
#             yield imframe
#             i += 1
#     except EOFError:
#         pass
#
# for i, frame in enumerate(iter_frames(im)):
#     frame.save('dash_g_%d.png' % i,**frame.info)


a = [[0] * 59 for _ in range(59)]
ans = 0
for i in range(59):
    for j in range(59):
        pram = 0
        if i - 18 >= 0:
            pram += 1
        if i + 18 < 59:
            pram += 1
        if j - 18 >= 0:
            pram += 1
        if j + 18 < 59:
            pram += 1
        a[i][j] = pram
        if pram >= 3:
            ans += 1

for i in a:
    print(i)
print(ans)