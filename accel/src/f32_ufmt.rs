use micromath::F32Ext;
use ufmt::uDisplay;

#[repr(transparent)]
pub struct ThreeFmt(pub f32);

impl uDisplay for ThreeFmt {
    fn fmt<W>(&self, fmt: &mut ufmt::Formatter<'_, W>) -> Result<(), W::Error>
        where
            W: ufmt::uWrite + ?Sized {
        let float = if self.0 < 0. {
            ufmt::uwrite!(fmt, "-")?;
            -self.0
        } else {
            self.0
        };

        let rounded = float.round();
        let shifted = ((float * 1000.) - rounded).round() as u64;
        let thousanth = shifted % 10;
        let hundreth = (shifted / 10) % 10;
        let tenth = (shifted / 100) % 10;
        
        ufmt::uwrite!(fmt, "{}.{}{}{}", rounded as u64, tenth, hundreth, thousanth)
    }
}
