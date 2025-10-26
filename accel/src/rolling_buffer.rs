use core::mem::MaybeUninit;

pub struct Collection<const LEN: usize> {
    arr: [MaybeUninit<f32>; LEN],
    len: usize,
    offset: usize,
}

impl<const LEN: usize> Collection<LEN> {
    pub fn new() -> Self {
        return Self {
            arr: [MaybeUninit::uninit(); LEN],
            len: 0,
            offset: 0
        }
    }

    pub fn push(&mut self, item: f32) {
        if self.len == LEN {
            self.arr[self.offset] = MaybeUninit::new(item);
            self.offset = (self.offset + 1) % LEN;
        } else {
            self.arr[self.len] = MaybeUninit::new(item);
            self.len += 1;
        }
    }

    pub fn avg(&self) -> f32 {
        let mut accum = 0.;

        for item in &self.arr[0..self.len] {
            accum += unsafe { item.assume_init_read() };
        }

        return accum / (self.len as f32);
    }

    pub fn clear(&mut self) {
        self.len = 0;
        self.offset = 0;
    }

    pub fn full(&self) -> bool {
        return self.len == LEN;
    }
}
