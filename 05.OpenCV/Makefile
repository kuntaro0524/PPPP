TARGET = test3
OBJS = test3.o 

CXX = g++      # 好きなコンパイラ
CXXFLAGS = -Wall -O2 # この辺は適当

# OpenCV のライブラリを指定
OPENCVINC = `pkg-config --cflags opencv`
OPENCVLIB = `pkg-config --libs opencv`

$(TARGET):$(OBJS)
	$(CXX) -o $@ $(OBJS) $(OPENCVLIB)

.cpp.o:
	$(CXX) -c -o $@ $< $(OBJINCS)
